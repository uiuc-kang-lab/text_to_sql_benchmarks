import argparse
import logging
import os

import numpy as np
import torch
import tqdm.autonotebook as tqdm
from transformers import AutoTokenizer
from vllm import LLM, SamplingParams

from utils import read_jsonl_file, write_jsonl_file


# Configure logging
def setup_logging(log_file):
    logging.basicConfig(
        level=logging.DEBUG,
        format="%(asctime)s - %(levelname)s - %(message)s",
        handlers=[logging.FileHandler(log_file, mode="w"), logging.StreamHandler()],
    )


def process_results(results, tokenizer, max_results_tokens=256):
    encoded = tokenizer.encode(results)
    if len(encoded) > max_results_tokens:
        return tokenizer.decode(encoded[:max_results_tokens]) + "...[TRUNCATED]"
    else:
        return results


def process_sql(sample, sql, tokenizer):
    messages = [
        {
            "role": "system",
            "content": "You are a judge that can check whether a given SQL correctly answers a given natural language user query. You'll be given Database Schema, Question, External Knowledge, SQL, logprob Score and its Execution Result.",
        }
    ]
    sql_prompt = (
        "-- SQL: {}\n".format(sql["content"])
        + "-- Execution Result #rows: {}\n".format(sql["num_rows"])
        + "-- Execution Result START\n{}\n".format(
            process_results(sql["result"], tokenizer)
        )
        + "-- END Execution Result\n"
    )
    messages += [
        {
            "role": "user",
            "content": (
                "-- Database Schema: \n{}\n".format(sample["mschema_prompt"])
                + "-- Question: {}\n".format(sample["question"])
                + "-- External Knowledge: {}\n".format(sample["evidence"])
                + sql_prompt
                + "-- Does SQL correctly answer Question?\n"
            ),
        }
    ]
    return tokenizer.apply_chat_template(
        messages, tokenize=False, add_generation_prompt=True, return_tensors="pt"
    )


def logits_processor(_, scores):
    index = scores[0].view(torch.uint16)
    scores = torch.full_like(scores, float("-inf"))
    scores[index] = 1
    return scores


@torch.no_grad()
def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--input_file", type=str, required=True)
    parser.add_argument("--output_dir", type=str, required=True)
    parser.add_argument("--model", type=str, default="models/reward", required=False)
    parser.add_argument("--max_tokens", type=int, default=1024 * 16)
    parser.add_argument("--batch_size", type=int, default=1024 * 16, required=False)
    parser.add_argument("--output_col", type=str, default="reward")
    parser.add_argument("--num_gpus", type=int, default=1)
    parser.add_argument("--partition_index", type=int, default=0)
    parser.add_argument("--num_partitions", type=int, default=1)

    args = parser.parse_args()

    os.makedirs(args.output_dir, exist_ok=True)

    # Setup logging
    log_file = os.path.join(args.output_dir, "reward.log")
    setup_logging(log_file)

    # Log command-line arguments
    logging.info("Starting reward script with arguments:")
    for arg, value in vars(args).items():
        logging.info(f"  {arg}: {value}")

    # Read data
    logging.info("Reading input data...")
    data = read_jsonl_file(args.input_file)
    data = np.array_split(data, args.num_partitions)[args.partition_index].tolist()
    logging.info(
        f"Data size after partitioning: {len(data)} items "
        f"(partition {args.partition_index + 1} of {args.num_partitions})"
    )

    # Prepare output directory
    out_file_name = (
        f"data_reward_{args.partition_index}-of-{args.num_partitions}.jsonl"
        if args.num_partitions > 1
        else "data_reward_all.jsonl"
    )
    out_file_path = os.path.join(args.output_dir, out_file_name)
    logging.info(f"Output file path: {out_file_path}")

    if os.path.exists(out_file_path):
        out_file_cache = read_jsonl_file(out_file_path)
        for i in range(len(data)):
            if data[i]["question_id"] != out_file_cache[i]["question_id"]:
                raise ValueError(f"Question ID mismatch: {data[i]['question_id']} != {out_file_cache[i]['question_id']}")
    else:
        out_file_cache = None

    tokenizer = AutoTokenizer.from_pretrained(args.model)
    assert tokenizer.padding_side == "right"

    mschema_prompts = {
        path: open(path+".mschema", "r").read()
        for path in set(datum["db_path"] for datum in data)
    }

    prompts, prompts_metadata = [], []
    for idx, datum in enumerate(tqdm.tqdm(data, desc="Generating prompts")):
        datum["mschema_prompt"] = mschema_prompts[datum["db_path"]]
        for sql, sql_values in datum["responses"].items():
            if sql_values["evaluation"] not in ["pass: ??", "pass: correct", "pass: incorrect"]:
                sql_values[args.output_col] = float("-inf")
                continue
            if out_file_cache is not None and sql in out_file_cache[idx]["responses"]:
                if sql_values["evaluation"] == out_file_cache[idx]["responses"][sql]["evaluation"]:
                    sql_values[args.output_col] = out_file_cache[idx]["responses"][sql][args.output_col]
                    continue
            prompts.append(process_sql(datum, sql_values, tokenizer))
            prompts_metadata.append(
                {
                    "idx": idx,
                    "sql": sql,
                }
            )

    model = LLM(
        model=args.model,
        dtype="bfloat16",
        trust_remote_code=True,
        gpu_memory_utilization=0.95,
        max_model_len=args.max_tokens,
        tensor_parallel_size=args.num_gpus,
        enable_prefix_caching=True,
    )
    sampling_params = SamplingParams(
        temperature=0, top_p=1.0, max_tokens=1, logits_processors=[logits_processor]
    )

    for batch_start in tqdm.tqdm(
        range(0, len(prompts), args.batch_size), desc="Generating responses"
    ):
        batch_pmd = prompts_metadata[batch_start : batch_start + args.batch_size]
        batch_prompts = prompts[batch_start : batch_start + args.batch_size]

        batch_responses = model.generate(
            batch_prompts,
            sampling_params,
            use_tqdm=True,
        )
        batch_scores = [
            (
                torch.tensor([output_i.outputs[0].token_ids[0]], dtype=torch.uint16)
                .view(torch.bfloat16)
                .item()
                if len(output_i.outputs[0].token_ids) > 0
                else float("-inf")
            )
            for output_i in batch_responses
        ]
        for pmd, score in zip(batch_pmd, batch_scores):
            data[pmd["idx"]]["responses"][pmd["sql"]][args.output_col] = score

    output_dir = os.path.dirname(out_file_path)
    if output_dir:
        os.makedirs(output_dir, exist_ok=True)
    write_jsonl_file(out_file_path, data)


if __name__ == "__main__":
    main()

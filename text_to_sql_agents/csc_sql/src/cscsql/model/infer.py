import argparse
import os.path
import random
from copy import deepcopy
from typing import List, Dict

from vllm import LLM, SamplingParams
from transformers import AutoTokenizer, AutoConfig
from vllm.lora.request import LoRARequest

from cscsql.utils.common_utils import CommonUtils, parse_response
from cscsql.utils.file_utils import FileUtils
from cscsql.utils.infer_utils import (build_stop_token_ids,
                                          build_execute_sql_result,
                                          build_selection_vote_execute_sql_result,
                                          run_eval_major_vote, run_eval_major_vote_table)


def make_prefix(dp: Dict, template_type='think',
                instruction_key='input_seq',
                current_few_shot=None,
                current_selection_vote_predict=None,
                prompt_mode="vote"):
    question_raw = dp[instruction_key] + dp.get("input", "")
    task_msg = "Please output only the final SQL query, starts with keyword `SELECT`."
    question_raw = question_raw.replace(task_msg, '')

    if prompt_mode == "table":
        task_msg = """Instructions:\n- Make sure you only output the information that is asked in the question. If the question asks for a specific column, make sure to only include that column in the SELECT clause, nothing more.\n- The generated query should return all of the information asked in the question without any missing or extra information.\n- Before generating the final SQL query, please think through the steps of how to write the query."""
        question_raw = question_raw.replace(task_msg, '')

        task_msg2 = "Your task is to understand the schema and generate a valid SQL query to answer the question."
        new_task_msg2 = "Your task is to understand the schema and determine which tables are needed to generate the SQL queries that answer the questions."
        question_raw = question_raw.replace(task_msg2, new_task_msg2)

    if template_type == 'think':
        omni_output_format = """Output Format:\nIn your answer, please enclose the generated SQL query in a code block:\n```sql\n-- Your SQL query\n```\n\nTake a deep breath and think step by step to find the correct SQL query.\n"""
        question_raw = question_raw.replace(omni_output_format, '')

        sql_output_msg = """Show your work in <think> </think> tags. And return the final SQLite SQL query that starts with keyword `SELECT` in <answer> </answer> tags, \
for example <answer>SELECT AVG(rating_score) FROM movies</answer>. """

        if current_selection_vote_predict is not None and prompt_mode == "vote":
            sql_output_msg = """Show your work in <think> </think> tags. And return the final selection answer 'A' or 'B' in <answer> </answer> tags, \
for example <answer>A</answer>. """
        elif prompt_mode == "table":
            sql_output_msg = """Show your work in <think> </think> tags. And return the selected tables separate by comma in <answer> </answer> tags, \
for example <answer>Table1, Table2, Table3 , ...</answer>. """

        prefix = f"""You first thinks about the reasoning process in the mind and then provides the user with the answer.\n\
{question_raw}

Output Format:
{sql_output_msg} 

Let me solve this step by step."""


    else:
        prefix = dp[instruction_key] + dp.get("input", "")

        # add selection vote
        if current_selection_vote_predict is not None and prompt_mode == "vote":
            omni_output_format = """Output Format:\nIn your answer, please enclose the generated SQL query in a code block:\n```sql\n-- Your SQL query\n```\n\nTake a deep breath and think step by step to find the correct SQL query.\n"""
            selection_output_format = """Output Format:\nIn your answer, please enclose the final selection answer 'A' or 'B' in <answer> </answer> tags\n\nTake a deep breath and think step by step to find the correct candidate.\n"""
            prefix = prefix.replace(omni_output_format, selection_output_format)

    # add few shot
    task_msg = "Database Schema:"
    new_task_msg = "Database Schema:"
    few_shot_msg = ""
    if current_few_shot is not None and len(current_few_shot) > 0:
        few_shot_msg = CommonUtils.build_few_shot_example_msg(current_few_shot)
        new_task_msg = f"{few_shot_msg}\n\n{new_task_msg}"
        prefix = prefix.replace(task_msg, new_task_msg)

    return prefix


def build_prompt(raw_input_dataset: List[Dict],
                 prompt_name: str,
                 link_table_results=None,
                 few_shot_results=None,
                 few_shot_num=0,
                 predict_sql_results=None,
                 selection_vote_predict_sql_results=None,
                 is_train=False,
                 shuffle_ab=False,
                 prompt_mode="merge",
                 raw_data: List[Dict] = None,
                 db_path=None,
                 db_full_schema_config=None,
                 max_model_len=None
                 ):
    new_input_dataset = []
    for index, item in enumerate(raw_input_dataset):
        raw_one = None
        if raw_data:
            raw_one = raw_data[index]
            db_id = raw_one['db_id']
            item['id'] = index
            item['db_id'] = db_id
            target_sql = raw_one.get('SQL', '')

        current_few_shot = None
        if few_shot_results is not None and few_shot_num > 0:
            all_current_few_shot = few_shot_results[index]
            current_few_shot = all_current_few_shot[:few_shot_num]

        current_predict = None
        if predict_sql_results is not None and isinstance(predict_sql_results, dict):
            current_predict = predict_sql_results[index]

        current_selection_vote_predict = None
        if selection_vote_predict_sql_results is not None \
                and isinstance(selection_vote_predict_sql_results, dict):
            if index not in selection_vote_predict_sql_results:
                continue
            current_selection_vote_predict = selection_vote_predict_sql_results[index]

            if shuffle_ab and random.choice([0, 1]) == 1:
                old_current_selection_vote_predict = deepcopy(current_selection_vote_predict)
                current_selection_vote_predict['sql1'] = old_current_selection_vote_predict['sql2']
                current_selection_vote_predict['sql2'] = old_current_selection_vote_predict['sql1']
                current_selection_vote_predict['res1'] = old_current_selection_vote_predict['res2']
                current_selection_vote_predict['res2'] = old_current_selection_vote_predict['res1']
                current_selection_vote_predict['sql1_correctness'] = old_current_selection_vote_predict[
                    'sql2_correctness']
                current_selection_vote_predict['sql2_correctness'] = old_current_selection_vote_predict[
                    'sql1_correctness']

            item['id'] = current_selection_vote_predict['id']
            item['db_id'] = current_selection_vote_predict['db_id']
            item['vote_top2_correctness'] = current_selection_vote_predict['vote_top2_correctness']
            item['sql1_correctness'] = current_selection_vote_predict['sql1_correctness']
            item['sql2_correctness'] = current_selection_vote_predict['sql2_correctness']

            if prompt_mode == "vote":
                target = 'A' if current_selection_vote_predict['sql1_correctness'] == 1 else 'B'
            else:
                if current_selection_vote_predict['sql1_correctness'] == 1:
                    target = current_selection_vote_predict['sql1']
                elif current_selection_vote_predict['sql2_correctness'] == 1:
                    target = current_selection_vote_predict['sql2']
                else:
                    pass

                target = target_sql
            item['output'] = target

        prompt = make_prefix(item,
                             template_type=prompt_name,
                             current_few_shot=current_few_shot,
                             current_selection_vote_predict=current_selection_vote_predict,
                             prompt_mode=prompt_mode)
        current_predict_tables = link_table_results[index] if link_table_results is not None else []
        new_prompt = CommonUtils.build_link_table_from_ddl(prompt, current_predict_tables)
        new_prompt = CommonUtils.build_revision_prompt(new_prompt, predict_result=current_predict)
        if prompt_mode == "vote":
            new_prompt = CommonUtils.build_selection_vote_prompt(new_prompt,
                                                                 predict_result=current_selection_vote_predict)
        elif prompt_mode == "merge":
            new_prompt = CommonUtils.build_merge_generate_prompt(new_prompt,
                                                                 predict_result=current_selection_vote_predict)
        elif prompt_mode == "table":
            db_uri = CommonUtils.get_db_path(db_root=db_path, db_id=db_id)
            db_full_schema = db_full_schema_config[db_id]

            link_column_names, link_tables, normal_tentative_schema = CommonUtils.extract_merge_schema_from_sql(
                sqls=[target_sql],
                db_uri=db_uri,
                db_full_schema=db_full_schema,
                question_id=index)
            item['output'] = link_tables
            item.pop('output_seq')

        item["input_seq"] = new_prompt
        new_input_dataset.append(item)

    return new_input_dataset


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("--pretrained_model_name_or_path", type=str, default="/fs/fast/u2021000902/previous_nvme/xxx")
    parser.add_argument("--input_file", type=str, help="the input file path (prompts)")
    parser.add_argument("--output_file", type=str, help="the output file path (results)")
    parser.add_argument("--tensor_parallel_size", type=int, help="the number of used GPUs", default=4)
    parser.add_argument("--gpu_memory_utilization", type=float, help="gpu_memory_utilization", default=0.95)
    parser.add_argument("--n", type=int, help="the number of generated responses", default=4)
    parser.add_argument("--seed", type=int, help="seed", default=42)
    parser.add_argument("--temperature", type=float, help="temperature of llm's sampling", default=1.0)
    parser.add_argument("--prompt_name", type=str, help="prompt name", default='')
    parser.add_argument("--link_tables", type=str, default=None, help="predict sql path", )
    parser.add_argument("--few_shot_num", type=int, default=0, help="few shot num")
    parser.add_argument("--db_path", type=str, help="database path")
    parser.add_argument("--gold_file", type=str, help="gold sql path", default="none")
    parser.add_argument("--gen_sqls", type=str, default="", help="gen_sqls")
    parser.add_argument("--selection_vote", type=str, default="none", help="selection_vote")
    parser.add_argument("--prompt_mode", type=str, default="merge", help="prompt_mode")
    parser.add_argument("--max_lora_rank", type=int, default=64, help="max_lora_rank")
    parser.add_argument("--shuffle_ab", type=int, default=0, help="shuffle_ab")
    parser.add_argument("--system_prompt", type=str, default="default", help="system_prompt")

    opt = parser.parse_args()
    print(opt)
    shuffle_ab = False if opt.shuffle_ab in ['0', 0] else True
    is_train = True if str(opt.db_path).find("train") > -1 else False

    max_model_len = 8192
    if is_train:
        max_model_len = 12000
    max_output_len = 1024  # (max_input_len + max_output_len) must <= max_model_len

    db_full_schema_config, db_sample_config = CommonUtils.get_all_db_full_schema_and_sample(db_root=opt.db_path)

    # get few shot example
    few_shot_results = None
    if opt.few_shot_num > 0:
        few_shot_results = CommonUtils.get_few_shot_list()

    predict_sql_results = build_execute_sql_result(opt.gen_sqls, db_path=opt.db_path)
    if opt.gen_sqls is not None and opt.gen_sqls not in ["none"] and predict_sql_results is None:
        print(f"predict_sql_results is None, please check your gen_sqls file, file name: {opt.gen_sqls}")

    selection_vote_predict_sql_results, all_predict_results = build_selection_vote_execute_sql_result(
        opt.selection_vote,
        db_path=opt.db_path,
        is_train=False,
        prompt_mode=opt.prompt_mode)

    if opt.selection_vote is not None \
            and opt.selection_vote not in ["none"] \
            and selection_vote_predict_sql_results is None:
        print("selection_vote_predict_sql_results is None, "
              "please check your selection_vote file, file name: {opt.selection_vote}")

    parse_mode = 'sql'
    if selection_vote_predict_sql_results is not None and opt.prompt_mode == 'vote':
        parse_mode = 'selection_vote'
    elif opt.prompt_mode == 'table':
        parse_mode = 'table'

    raw_input_dataset = FileUtils.load_json(opt.input_file)
    raw_data = FileUtils.load_json(str(opt.db_path).replace("_databases", ".json"))

    link_table_results = CommonUtils.read_link_table(link_table_files=opt.link_tables,
                                                     is_train=is_train)

    input_dataset = build_prompt(raw_input_dataset,
                                 prompt_name=opt.prompt_name,
                                 link_table_results=link_table_results,
                                 few_shot_results=few_shot_results,
                                 few_shot_num=opt.few_shot_num,
                                 predict_sql_results=predict_sql_results,
                                 selection_vote_predict_sql_results=selection_vote_predict_sql_results,
                                 shuffle_ab=shuffle_ab,
                                 is_train=is_train,
                                 prompt_mode=opt.prompt_mode,
                                 raw_data=raw_data,
                                 db_path=opt.db_path,
                                 db_full_schema_config=db_full_schema_config,
                                 max_model_len=max_model_len
                                 )

    enable_lora = False
    lora_request = None
    model_path = opt.pretrained_model_name_or_path
    lora_config_path = os.path.join(model_path, "adapter_config.json")
    if os.path.exists(lora_config_path):
        enable_lora = True
        lora_config = FileUtils.load_json(lora_config_path)
        model_path = lora_config.get("base_model_name_or_path", model_path)
        epoch = 1
        try:
            epoch = int(str(opt.pretrained_model_name_or_path).split("-")[-1])
        except:
            pass
        lora_request = LoRARequest(f"sft_adapter_{epoch}", epoch, opt.pretrained_model_name_or_path)
        print(f"use lora: r={lora_config['r']} lora_alpha={lora_config['lora_alpha']}")

    tokenizer = AutoTokenizer.from_pretrained(model_path, trust_remote_code=True)
    config = AutoConfig.from_pretrained(model_path, trust_remote_code=True)
    stop_token_ids = config.eos_token_id if hasattr(config, "eos_token_id") else None
    if isinstance(stop_token_ids, int):
        stop_token_ids = [stop_token_ids]

    print("parse_mode:", parse_mode)
    print("max_model_len:", max_model_len)
    print("temperature:", opt.temperature)
    print("n:", opt.n)
    print("few_shot_num:", opt.few_shot_num)
    print("stop_token_ids:", stop_token_ids)
    sampling_params = SamplingParams(
        temperature=opt.temperature,
        max_tokens=max_output_len,
        n=opt.n,
        stop_token_ids=stop_token_ids
    )

    llm = LLM(
        model=model_path,
        dtype="bfloat16",
        tensor_parallel_size=opt.tensor_parallel_size,
        max_model_len=max_model_len,
        seed=opt.seed,
        gpu_memory_utilization=opt.gpu_memory_utilization,
        swap_space=42,
        enforce_eager=True,
        enable_lora=enable_lora,
        max_lora_rank=opt.max_lora_rank,
        disable_custom_all_reduce=True,
        trust_remote_code=True
    )

    system_prompt = "You are a helpful AI Assistant that provides well-reasoned and detailed responses. You first think about the reasoning process as an internal monologue and then provide the user with the answer. Respond in the following format: <think>\n...\n</think>\n<answer>\n...\n</answer>"

    chat_prompts = []
    for data in input_dataset:
        messages = []
        if opt.system_prompt == "none":
            system_prompt = ""
        elif opt.system_prompt == "default":
            system_prompt = system_prompt
        else:
            system_prompt = opt.system_prompt

        if len(system_prompt) > 10:
            messages.append({"role": "system", "content": system_prompt})

        messages.append({"role": "user", "content": data["input_seq"]})
        res = tokenizer.apply_chat_template(messages,
                                            add_generation_prompt=True,
                                            tokenize=False)

        chat_prompts.append(res)

    print(f"prompt[0]:")
    print(chat_prompts[0])

    outputs = llm.generate(chat_prompts,
                           sampling_params=sampling_params,
                           lora_request=lora_request, )

    results = []
    for data, output in zip(input_dataset, outputs):
        responses = [o.text for o in output.outputs]
        sqls = [parse_response(response, mode=parse_mode) for response in responses]

        data["responses"] = responses
        data["pred_sqls"] = sqls
        results.append(data)

    print(f"responses[0]:")
    print(results[0]["responses"][0])
    print(f"pred_sqls[0]:")
    print(results[0]["pred_sqls"][0])

    if all_predict_results and len(all_predict_results) == len(raw_data):
        infer_ids = [item['id'] for item in results]
        for index, item in enumerate(all_predict_results):
            if item['id'] not in infer_ids:
                new_item = deepcopy(item)
                new_item['mode'] = "major_vote"
                new_item['pred_sqls'] = [item['sql'] for _ in range(opt.n)]
                new_item['responses'] = new_item['pred_sqls']
                results.append(new_item)

    results.sort(key=lambda x: int(x['id']))
    FileUtils.dump_json(opt.output_file, results)

    if parse_mode == "sql":
        run_eval_major_vote(gold_file=opt.gold_file,
                            pred_file=opt.output_file,
                            db_path=opt.db_path,
                            config=opt.__dict__)

    if parse_mode == "table" and len(opt.gold_file) > 10:
        run_eval_major_vote_table(gold_file=opt.gold_file,
                                  pred_file=opt.output_file,
                                  db_path=opt.db_path,
                                  config=opt.__dict__)

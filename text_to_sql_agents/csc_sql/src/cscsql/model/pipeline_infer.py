import os
import argparse

from cscsql.utils.file_utils import FileUtils
from cscsql.utils.time_utils import TimeUtils

RUN_TIME = TimeUtils.now_str_short()


def run_eval_by_cmd(opt, eval_mode="greedy_search", eval_step=None):
    if eval_step == "table_link":
        use_model = opt.model_table_link
        opt.prompt_mode = "table"
        n = opt.n_table_link
        temperature = opt.temperature_table_link
    elif eval_step == "sql_generate":
        use_model = opt.model_sql_generate
        opt.prompt_mode = "merge"
        n = opt.n_sql_generate
        temperature = opt.temperature_sql_generate
    elif eval_step == "sql_merge":
        use_model = opt.model_sql_merge
        opt.prompt_mode = "merge"
        opt.link_tables = "none"
        n = opt.n_sql_merge
        temperature = opt.temperature_sql_merge
    else:
        use_model = opt.model_sql_generate
        n = opt.n_sql_generate
        temperature = opt.temperature_sql_generate

    if eval_mode == "greedy_search":
        n = 1
        temperature = 0.0
        prefix = eval_mode
    else:
        prefix = "sampling"

    print(f"eval step: {eval_step} - use_model: {use_model}")
    pretrained_model_name_or_path = use_model

    output_dir = os.path.join(opt.output_dir, opt.run_time)
    os.makedirs(output_dir, exist_ok=True)

    show_prefix = f"{prefix}_{opt.prompt_name}_{eval_step}"
    gs_pred_file = f"{output_dir}/{show_prefix}.json"
    print(f"Evaluating output dir: {gs_pred_file}")

    print(opt)
    FileUtils.dump_json(f"{output_dir}/arg_{eval_step}.json", opt.__dict__)

    greedy_search_cmd = f"CUDA_VISIBLE_DEVICES={opt.visible_devices} python3 -m cscsql.model.infer  \
        --pretrained_model_name_or_path {pretrained_model_name_or_path} \
        --input_file {opt.input_file} \
        --output_file {gs_pred_file} \
        --db_path {opt.db_path} \
        --gold_file {opt.gold_file} \
        --tensor_parallel_size {opt.tensor_parallel_size} \
        --gpu_memory_utilization {opt.gpu_memory_utilization} \
        --prompt_name {opt.prompt_name} \
        --prompt_mode {opt.prompt_mode} \
        --link_tables {opt.link_tables} \
        --gen_sqls {opt.gen_sqls} \
        --selection_vote {opt.selection_vote} \
        --few_shot_num {opt.max_few_shot} \
        --seed {opt.seed} \
        --n {n} \
        --temperature {temperature}"
    os.system(greedy_search_cmd)

    vote_file = gs_pred_file[:-5] + "_pred_major_voting_sqls.sql"
    print(f"finish infer step {eval_step} - {use_model}, result file: {vote_file}")

    return gs_pred_file


def run_eval_pipeline(opt, eval_mode="greedy_search", eval_step=None):
    if eval_step in ["pipeline", "sql_pipeline"]:
        if eval_step == "pipeline":
            table_link_file = run_eval_by_cmd(opt=opt, eval_mode=eval_mode, eval_step="table_link")

            opt.link_tables = table_link_file
        sql_generate_file = run_eval_by_cmd(opt=opt, eval_mode=eval_mode, eval_step="sql_generate")
        # result_file = sql_generate_file
        opt.selection_vote = sql_generate_file
        result_file = run_eval_by_cmd(opt=opt, eval_mode=eval_mode, eval_step="sql_merge")
    else:
        result_file = run_eval_by_cmd(opt=opt, eval_mode=eval_mode, eval_step=eval_step)

    vote_file = result_file[:-5] + "_pred_major_voting_sqls.sql"
    print(f"finish all {eval_step} - {eval_mode} -\n"
          f"result_file: {vote_file}")
    return result_file


if __name__ == "__main__":
    parser = argparse.ArgumentParser()

    parser.add_argument("--model_table_link", type=str, help="table link model")
    parser.add_argument("--model_sql_generate", type=str, help="sql generate model")
    parser.add_argument("--model_sql_merge", type=str, help="sql merge model")
    parser.add_argument("--source", type=str, default="bird")
    parser.add_argument("--input_file", type=str, help="input file path (prompts)")
    parser.add_argument("--gold_file", type=str, help="gold sql path", default="none")
    parser.add_argument("--db_path", type=str, help="database path")
    parser.add_argument("--run_time", type=str, default=None)
    parser.add_argument("--output_dir", type=str, default="outputs")
    parser.add_argument("--eval_name", type=str, help="name of the evaluation set", default="qwen2.5_coder_7b")
    parser.add_argument("--visible_devices", type=str, default="0")
    parser.add_argument("--tensor_parallel_size", type=int, help="the number of used GPUs", default=1)
    parser.add_argument("--gpu_memory_utilization", type=float, help="gpu_memory_utilization", default=0.95)
    parser.add_argument("--seed", type=int, help="seed", default=42)

    parser.add_argument("--eval_step", type=str, default="pipeline",
                        help="eval step, choice: [table_link, sql_generate, sql_merge, pipeline ]")
    parser.add_argument("--eval_mode", type=str, help="eval_mode", default='major_voting')
    parser.add_argument("--n_table_link", type=int, help="sampling number for table_link", default=8)
    parser.add_argument("--temperature_table_link", type=float, help="sampling temperature for table_link", default=0.8)
    parser.add_argument("--n_sql_generate", type=int, help="sampling number for sql_generate", default=8)
    parser.add_argument("--temperature_sql_generate", type=float, help="sampling temperature for sql_generate",
                        default=0.8)
    parser.add_argument("--n_sql_merge", type=int, help="sampling number for sql_merge", default=8)
    parser.add_argument("--temperature_sql_merge", type=float, help="sampling temperature for sql_merge", default=0.8)
    parser.add_argument("--prompt_name", type=str, help="prompt name", default='think')
    parser.add_argument("--run_comment", type=str, help="run_comment", default='')
    parser.add_argument("--link_tables", type=str, default="none", help="predict sql path")
    parser.add_argument("--max_few_shot", type=int, default=0, help="few shot num")
    parser.add_argument("--gen_sqls", type=str, default="none", help="predict generate sql file")
    parser.add_argument("--selection_vote", type=str, default="none", help="selection_vote")
    parser.add_argument("--prompt_mode", type=str, default="merge", help="prompt_mode")

    opt = parser.parse_args()
    if opt.run_time is None:
        opt.run_time = RUN_TIME

    output_dir = os.path.join(opt.output_dir, opt.run_time)
    os.makedirs(output_dir, exist_ok=True)

    eval_mode_list = opt.eval_mode.lower().split(",")
    if eval_mode_list == ["all"]:
        eval_mode_list = ["greedy_search", "major_voting"]

    assert opt.source in ["spider", "bird", "spider2.0"]

    if "greedy_search" in eval_mode_list:
        # greedy decoding
        run_eval_pipeline(opt=opt,
                          eval_mode="greedy_search",
                          eval_step=opt.eval_step)
    else:
        print(f"skip greedy search")

    if "major_voting" in eval_mode_list:
        # sampling
        run_eval_pipeline(opt=opt,
                          eval_mode="major_voting",
                          eval_step=opt.eval_step)
    else:
        print(f"skip pass at k and major voting")

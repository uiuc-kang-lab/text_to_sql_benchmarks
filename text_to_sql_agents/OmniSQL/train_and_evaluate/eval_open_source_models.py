import os

models = [
    "seeklhy/OmniSQL-7B",
    "seeklhy/OmniSQL-14B",
    "seeklhy/OmniSQL-32B",
    # "qwen/Qwen2.5-Coder-7B-Instruct",
    # "qwen/Qwen2.5-Coder-14B-Instruct",
    # "qwen/Qwen2.5-Coder-32B-Instruct",
    # "qwen/Qwen2.5-7B-Instruct",
    # "qwen/Qwen2.5-14B-Instruct",
    # "qwen/Qwen2.5-32B-Instruct",
    # "qwen/Qwen2.5-72B-Instruct",
    # "meta-llama/Meta-Llama-3.1-8B-Instruct",
    # "meta-llama/Meta-Llama-3.1-70B-Instruct",
    # "infly/OpenCoder-8B-Instruct",
    # "deepseek-ai/deepseek-coder-6.7b-instruct",
    # "deepseek-ai/deepseek-coder-33b-instruct",
    # "deepseek-ai/deepseek-v3",
    # "ibm-granite/granite-34b-code-instruct-8k",
    # "ibm-granite/granite-20b-code-instruct-8k",
    # "ibm-granite/granite-8b-code-instruct-128k",
    # "ibm-granite/granite-3.1-8b-instruct",
    # "deepseek-ai/DeepSeek-Coder-V2-Lite-Instruct",
    # "bigcode/starcoder2-15b-instruct-v0.1",
    # "mistralai/Codestral-22B-v0.1",
    # "mistralai/Mixtral-8x7B-Instruct-v0.1",
]

visible_devices = "0,1" # visible devices for vLLM
tensor_parallel_size = len(visible_devices.split(","))

for model in models:
    model_name = model.split("/")[-1].strip()

    spider2_test_eval_name = f"{model_name}_test_spider2_sqlite"
    spider2_test_evaluation_cmd = f"python3 auto_evaluation.py --output_ckpt_dir {model} --source spider2.0 --visible_devices {visible_devices} --input_file ./data/test_spider2_sqlite.json --eval_name {spider2_test_eval_name} --tensor_parallel_size {tensor_parallel_size} --n 8 --gold_file ./data/spider2_sqlite/test.json --db_path ./data/spider2_sqlite/databases/ --gold_result_dir ./data/spider2_sqlite/gold_exec_result/ --eval_standard ./data/spider2_sqlite/spider2_sqlite_eval.jsonl"
    os.system(spider2_test_evaluation_cmd)

    dev_bird_eval_name = f"{model_name}_dev_bird"
    dev_bird_evaluation_cmd = f"python3 auto_evaluation.py --output_ckpt_dir {model} --source bird --visible_devices {visible_devices} --input_file ./data/dev_bird.json --eval_name {dev_bird_eval_name} --tensor_parallel_size {tensor_parallel_size} --n 8 --gold_file ./data/bird/dev_20240627/dev.json --db_path ./data/bird/dev_20240627/dev_databases"
    os.system(dev_bird_evaluation_cmd)

    dev_spider_eval_name = f"{model_name}_dev_spider"
    dev_spider_evaluation_cmd = f"python3 auto_evaluation.py --output_ckpt_dir {model} --source spider --visible_devices {visible_devices} --input_file ./data/dev_spider.json --eval_name {dev_spider_eval_name} --tensor_parallel_size {tensor_parallel_size} --n 8 --gold_file ./data/spider/dev_gold.sql --db_path ./data/spider/database --ts_db_path ./test_suite_sql_eval/test_suite_database"
    os.system(dev_spider_evaluation_cmd)

    test_spider_eval_name = f"{model_name}_test_spider"
    test_spider_evaluation_cmd = f"python3 auto_evaluation.py --output_ckpt_dir {model} --source spider --visible_devices {visible_devices} --input_file ./data/test_spider.json --eval_name {test_spider_eval_name} --tensor_parallel_size {tensor_parallel_size} --n 8 --gold_file ./data/spider/test_gold.sql --db_path ./data/spider/test_database"
    os.system(test_spider_evaluation_cmd)

    spider_dk_eval_name = f"{model_name}_dev_spider_dk"
    spider_dk_evaluation_cmd = f"python3 auto_evaluation.py --output_ckpt_dir {model} --source spider --visible_devices {visible_devices} --input_file ./data/dev_spider_dk.json --eval_name {spider_dk_eval_name} --tensor_parallel_size {tensor_parallel_size} --n 8 --gold_file ./data/Spider-DK/spider_dk_gold.sql --db_path ./data/Spider-DK/database"
    os.system(spider_dk_evaluation_cmd)

    spider_realistic_eval_name = f"{model_name}_dev_spider_realistic"
    spider_realistic_evaluation_cmd = f"python3 auto_evaluation.py --output_ckpt_dir {model} --source spider --visible_devices {visible_devices} --input_file ./data/dev_spider_realistic.json --eval_name {spider_realistic_eval_name} --tensor_parallel_size {tensor_parallel_size} --n 8 --gold_file ./data/spider-realistic/spider_realistic_gold.sql --db_path ./data/spider/database --ts_db_path ./test_suite_sql_eval/test_suite_database"
    os.system(spider_realistic_evaluation_cmd)

    spider_syn_eval_name = f"{model_name}_dev_spider_syn"
    spider_syn_evaluation_cmd = f"python3 auto_evaluation.py --output_ckpt_dir {model} --source spider --visible_devices {visible_devices} --input_file ./data/dev_spider_syn.json --eval_name {spider_syn_eval_name} --tensor_parallel_size {tensor_parallel_size} --n 8 --gold_file ./data/Spider-Syn/spider_syn_gold.sql --db_path ./data/spider/database --ts_db_path ./test_suite_sql_eval/test_suite_database"
    os.system(spider_syn_evaluation_cmd)

    dev_ehrsql_eval_name = f"{model_name}_dev_ehrsql"
    dev_ehrsql_evaluation_cmd = f"python3 auto_evaluation.py --output_ckpt_dir {model} --source bird --visible_devices {visible_devices} --input_file ./data/dev_ehrsql.json --eval_name {dev_ehrsql_eval_name} --tensor_parallel_size {tensor_parallel_size} --n 8 --gold_file ./data/EHRSQL/dev.json --db_path ./data/EHRSQL/database"
    os.system(dev_ehrsql_evaluation_cmd)

    dev_sciencebenchmark_eval_name = f"{model_name}_dev_sciencebenchmark"
    dev_sciencebenchmark_evaluation_cmd = f"python3 auto_evaluation.py --output_ckpt_dir {model} --source bird --visible_devices {visible_devices} --input_file ./data/dev_sciencebenchmark.json --eval_name {dev_sciencebenchmark_eval_name} --tensor_parallel_size {tensor_parallel_size} --n 8 --gold_file ./data/sciencebenchmark/dev.json --db_path ./data/sciencebenchmark/databases"
    os.system(dev_sciencebenchmark_evaluation_cmd)
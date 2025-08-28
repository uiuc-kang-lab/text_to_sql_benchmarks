# import debugpy; debugpy.connect(('127.0.0.1', 5688))
import json
import re
import pandas as pd
import math
# import duckdb
from typing import List, Union
import os
import os.path as osp
import pandas as pd
import argparse
# from google.cloud import bigquery
import shutil
import multiprocessing as mp
import sqlite3
from tqdm import tqdm
# import snowflake.connector
import logging
from func_timeout import func_timeout, FunctionTimedOut
import sys
from functools import partial
import tempfile

class TeeOutput:
    def __init__(self, filename):
        self.console = sys.stdout
        self.file = open(filename, 'w')
    
    def write(self, message):
        self.console.write(message)
        self.file.write(message)
    
    def flush(self):
        self.console.flush()
        self.file.flush()
    
    def close(self):
        self.file.close()

sys.stdout = TeeOutput('log.txt')
sys.stderr = sys.stdout

TOTAL_GB_PROCESSED = 0.0


byte_output_dict = {}

def load_jsonl_to_dict(jsonl_file):
    data_dict = {}
    with open(jsonl_file, 'r') as file:
        for line in file:
            item = json.loads(line.strip())
            instance_id = item['instance_id']
            data_dict[instance_id] = item
    return data_dict

def load_json_list_to_dict(json_file_path):
    with open(json_file_path, 'r', encoding='utf-8') as file:
        data_list = json.load(file)
    data_dict = {item['instance_id']: item for item in data_list}
    return data_dict

def compare_multi_pandas_table(pred, multi_gold, multi_condition_cols, multi_ignore_order):
    # print('multi_condition_cols', multi_condition_cols)
    # print("len(multi_condition_cols)", len(multi_condition_cols))

    if multi_condition_cols == [] or multi_condition_cols == [[]] or multi_condition_cols == [None] or multi_condition_cols == None:
        multi_condition_cols = [[] for _ in range(len(multi_gold))]
    elif len(multi_gold) > 1 and not all(isinstance(sublist, list) for sublist in multi_condition_cols):
        multi_condition_cols = [multi_condition_cols for _ in range(len(multi_gold))]
    # multi_ignore_order = [multi_ignore_order for _ in range(len(multi_gold))]

    assert len(multi_gold) == len(multi_condition_cols) == len(multi_ignore_order)

    for i, gold in enumerate(multi_gold):
        if compare_pandas_table(pred, gold, multi_condition_cols[i], multi_ignore_order[i]):
            return 1
    return 0

def compare_pandas_table(pred, gold, condition_cols=[], ignore_order=False):
    """_summary_

    Args:
        pred (Dataframe): _description_
        gold (Dataframe): _description_
        condition_cols (list, optional): _description_. Defaults to [].
        ignore_order (bool, optional): _description_. Defaults to False.

    """
    # print('condition_cols', condition_cols)
    
    tolerance = 1e-2

    def vectors_match(v1, v2, tol=tolerance, ignore_order_=False):
        if ignore_order_:
            v1, v2 = (sorted(v1, key=lambda x: (x is None, str(x), isinstance(x, (int, float)))),
                    sorted(v2, key=lambda x: (x is None, str(x), isinstance(x, (int, float)))))
        if len(v1) != len(v2):
            return False
        for a, b in zip(v1, v2):
            if pd.isna(a) and pd.isna(b):
                continue
            elif isinstance(a, (int, float)) and isinstance(b, (int, float)):
                if not math.isclose(float(a), float(b), abs_tol=tol):
                    return False
            elif a != b:
                return False
        return True
    
    if condition_cols != []:
        gold_cols = gold.iloc[:, condition_cols]
    else:
        gold_cols = gold
    pred_cols = pred

    t_gold_list = gold_cols.transpose().values.tolist()
    t_pred_list = pred_cols.transpose().values.tolist()
    score = 1
    for _, gold in enumerate(t_gold_list):
        if not any(vectors_match(gold, pred, ignore_order_=ignore_order) for pred in t_pred_list):
            score = 0
        else:
            for j, pred in enumerate(t_pred_list):
                if vectors_match(gold, pred, ignore_order_=ignore_order):
                    break

    return score

def get_sqlite_result(db_file_path, query, save_dir=None, file_name="result.csv", chunksize=500):
    conn = sqlite3.connect(db_file_path)
    memory_conn = sqlite3.connect(':memory:')

    conn.backup(memory_conn)
    
    try:
        if save_dir:
            if not os.path.exists(save_dir):
                os.makedirs(save_dir)
            for i, chunk in enumerate(pd.read_sql_query(query, memory_conn, chunksize=chunksize)):
                mode = 'a' if i > 0 else 'w'
                header = i == 0
                chunk.to_csv(os.path.join(save_dir, file_name), mode=mode, header=header, index=False)
        else:
            df = pd.read_sql_query(query, memory_conn)
            return True, df

    except Exception as e:
        print(f"An error occurred: {e}")
        return False, str(e)

    finally:
        memory_conn.close()
        conn.close()
    
    return True, None

def evaluate_spider2sql(gold_result_dir, eval_standard_dict, gold, pred_sqls, db_path, temp_dir):
    instance_id2db_id = dict()
    for gt_data in gold:
        instance_id2db_id[gt_data["instance_id"]] = gt_data["db_id"]
    
    instance_id2pred_sql_query = dict()
    for gt_data, pred_sql in zip(gold, pred_sqls):
        instance_id2pred_sql_query[gt_data["instance_id"]] =  pred_sql
    
    eval_ids = list(eval_standard_dict.keys())
    assert len(gold) == len(pred_sqls) == len(eval_ids)

    output_results = []
    for instance_id in tqdm(eval_ids):
        print(f">>>Evaluating {instance_id}...")
        if instance_id not in instance_id2pred_sql_query:
            raise ValueError("instance id '{instance_id}' not in instance_id2pred_sql_query")
        if instance_id not in instance_id2db_id:
            raise ValueError("instance id '{instance_id}' not in instance_id2db_id")

        error_info = None
        pred_sql_query = instance_id2pred_sql_query[instance_id]
        db_file_path = os.path.join(db_path, instance_id2db_id[instance_id], instance_id2db_id[instance_id] + ".sqlite")
        exe_flag, dbms_error_info = get_sqlite_result(db_file_path, pred_sql_query, temp_dir, f"{instance_id}_pred.csv")
        if exe_flag == False:
            score = 0
            error_info = dbms_error_info
        else:
            pred_pd = pd.read_csv(os.path.join(temp_dir, f"{instance_id}_pred.csv"))  
            pattern = re.compile(rf'^{re.escape(instance_id)}(_[a-z])?\.csv$')

            all_files = os.listdir(gold_result_dir)
            csv_files = [file for file in all_files if pattern.match(file)]
            if len(csv_files) == 1:
                gold_pd = pd.read_csv(os.path.join(gold_result_dir, f"{instance_id}.csv"))
                try:
                    score = compare_pandas_table(pred_pd, gold_pd, eval_standard_dict.get(instance_id)['condition_cols'], eval_standard_dict.get(instance_id)['ignore_order'])
                except Exception as e:
                    print(f"An error occurred: {e}")
                    score = 0
                    error_info = 'Python Script Error:' + str(e)
                if score == 0 and error_info is None:
                    error_info = 'Result Error'     
                # print("score:", score)
                # print("pred_pd:\n", pred_pd)
                # print("gold_pd:\n", gold_pd)

            elif len(csv_files) > 1:
                gold_pds = [pd.read_csv(os.path.join(gold_result_dir, file)) for file in csv_files]
                score = compare_multi_pandas_table(pred_pd, gold_pds, eval_standard_dict.get(instance_id)['condition_cols'], eval_standard_dict.get(instance_id)['ignore_order'])
                if score == 0 and error_info is None:
                    error_info = 'Result Error'
                # print("score:", score)
                # print("pred_pd:\n", pred_pd)
                # print("gold_pds:\n", gold_pds)

        output_results.append(
            {
                "instance_id": instance_id, 
                "score": score,
                "pred_sql": pred_sql_query,
                "error_info": error_info
            }
        )

    print({item['instance_id']: item['score'] for item in output_results})
    final_acc = sum([item['score'] for item in output_results]) / len(output_results)
    print(f"Final score: {final_acc}")
    print("Correct Instance ID:")
    for item in output_results:
        if item["score"] == 1:
            print(item["instance_id"])
    return output_results, final_acc

def execute_sql(data_idx, db_file, sql):
    conn = sqlite3.connect(db_file)
    cursor = conn.cursor()
    try:
        conn.execute("BEGIN TRANSACTION;")
        cursor.execute(sql)
        execution_res = cursor.fetchall()
        execution_res = frozenset(execution_res) # make set hashable
        conn.rollback()
        conn.close()
        return {"data_idx": data_idx, "sql": sql, "execution_res": execution_res, "valid_flag": 1}
    except:
        conn.rollback()
        conn.close()
        return {"data_idx": data_idx, "sql": sql, "execution_res": None, "valid_flag": 0}

def execute_sql_wrapper(data_idx, db_file, sql, timeout):
    try:
        res = func_timeout(timeout, execute_sql, args=(data_idx, db_file, sql))
    except KeyboardInterrupt:
        sys.exit(0)
    except FunctionTimedOut:
        res = {"data_idx": data_idx, "sql": sql, "execution_res": None, "valid_flag": 0}
    except Exception as e:
        res = {"data_idx": data_idx, "sql": sql, "execution_res": None, "valid_flag": 0}

    return res

def execute_callback_execute_sqls(result, all_execution_results):
    # print("Done:", result["data_idx"])
    all_execution_results.append(result)

def execute_sqls_parallel(all_db_files, all_sqls, all_execution_results, num_cpus=10, timeout=30):
    pool = mp.Pool(processes=num_cpus)
    for data_idx, db_file, sql in zip(list(range(len(all_sqls))), all_db_files, all_sqls):
        callback_with_results = partial(execute_callback_execute_sqls, all_execution_results=all_execution_results)
        pool.apply_async(execute_sql_wrapper, args=(data_idx, db_file, sql, timeout), callback = callback_with_results)
    pool.close()
    pool.join()

def evaluate(mode, gold_result_dir, eval_standard, gold_file, pred_file, db_path, save_pred_sqls):
    eval_standard_dict = load_jsonl_to_dict(eval_standard)
    gold = json.load(open(gold_file))
    pred = json.load(open(pred_file))
    pred_sql_key = "pred_sqls"
    # pred_sql_key = "responses"

    sampling_num = len(pred[0][pred_sql_key])
    print(f"sampling_num: {sampling_num}")

    all_db_files = []
    all_pred_sqls = []
    for gold_data, pred_data in tqdm(zip(gold, pred)):
        db_file = os.path.join(db_path, gold_data["db_id"], gold_data["db_id"] + ".sqlite")
        for sample_idx in range(sampling_num):
            all_db_files.append(db_file)
            all_pred_sqls.append(pred_data[pred_sql_key][sample_idx])
    # obtain execution results of all predicted SQL queries
    all_execution_results = []
    execute_sqls_parallel(all_db_files, all_pred_sqls, all_execution_results, num_cpus=40, timeout=10)
    all_execution_results = sorted(all_execution_results, key=lambda x: x["data_idx"])
    print([res["data_idx"] for res in all_execution_results])
    
    pred_sqls = []
    for idx in range(len(gold)):
        execution_results = all_execution_results[idx*sampling_num: (idx+1)*sampling_num]
        if mode == "greedy_search":
            # For greedy_search calculation, pred_sqls is a list of SQL query strings.
            assert len(execution_results) == len(pred[0][pred_sql_key]) == sampling_num == 1
            if execution_results[0]["valid_flag"] == 1:
                pred_sqls.append(execution_results[0]["sql"])
            else:
                pred_sqls.append("Error SQL qeury")
        elif mode == "major_voting":
            # For major_voting calculation, pred_sqls is a list of SQL query strings.
            assert len(execution_results) == len(pred[0][pred_sql_key]) == sampling_num
            # no one pred sql is valid
            if sum(res["valid_flag"] for res in execution_results) == 0:
                pred_sqls.append("Error SQL qeury")
                continue

            major_voting_counting = dict()
            for res in execution_results:
                if res["valid_flag"] == 0:
                    continue
                if res["execution_res"] in major_voting_counting:
                    major_voting_counting[res["execution_res"]][0] += 1
                else:
                    major_voting_counting[res["execution_res"]] = [1, res["sql"]]
            major_vote = max(major_voting_counting.values(), key=lambda x: x[0])
            mj_pred_sql = major_vote[1]
            pred_sqls.append(mj_pred_sql)
        elif mode == "pass@k":
            # For pass@k calculation, pred_sqls is a list where each element is a list of SQL query strings.
            assert len(execution_results) == len(pred[0][pred_sql_key]) == sampling_num
            pred_sqls.append([res["sql"] if res["valid_flag"] == 1 else "Error SQL query" for res in execution_results])

    assert len(pred_sqls) == len(gold) == len(pred)

    if mode in ["greedy_search", "major_voting"]:
        temp_dir = tempfile.mkdtemp(prefix="temp-") # , dir="./"
        print("temp_dir:", temp_dir)
        output_results, final_acc = evaluate_spider2sql(
            gold_result_dir,
            eval_standard_dict,
            gold,
            pred_sqls,
            db_path,
            temp_dir
        )

        if save_pred_sqls:
            suffix = "-pred-greedy-search-sqls.json" if mode == "greedy_search" else "-pred-major-voting-sqls.json"
            with open(pred_file[:-5] + suffix, "w", encoding="utf-8") as f:
                f.write(json.dumps(pred_sqls, indent=2 ,ensure_ascii=False))

        print(f"{mode} ACC: {final_acc}")
        if os.path.exists(temp_dir):
            shutil.rmtree(temp_dir)
        return final_acc, pred_sqls
    elif mode == "pass@k":
        all_scores = []
        for sample_idx in range(sampling_num):
            temp_dir = tempfile.mkdtemp(prefix="temp-") # , dir="./"
            print("temp_dir:", temp_dir)
            pred_sqls_for_specific_sample_idx = [sqls[sample_idx] for sqls in pred_sqls]
            output_results, _ = evaluate_spider2sql(
                gold_result_dir,
                eval_standard_dict,
                gold,
                pred_sqls_for_specific_sample_idx,
                db_path,
                temp_dir
            )
            all_scores.append([item['score'] for item in output_results])
            if os.path.exists(temp_dir):
                shutil.rmtree(temp_dir)
        print(all_scores)
        pass_at_k_scores = [1 if any(column) else 0 for column in zip(*all_scores)]
        final_acc = sum(pass_at_k_scores)/len(pass_at_k_scores)
        print(pass_at_k_scores)
        print(f"{mode} ACC: {final_acc}")
        return final_acc, None

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Run evaluations for NLP models.")
    parser.add_argument("--mode", type=str, choices=["greedy_search", "major_voting", "pass@k"])
    parser.add_argument("--pred", type=str, default="../results/Qwen2.5-Coder-7B-Instruct-spider2.0-test-greedy.json", help="Predicted result directory")
    parser.add_argument('--gold', type = str, default = "./data/spider2.0/test.json")
    parser.add_argument('--gold_result_dir', type = str, default = "./data/spider2.0/gold_exec_result")
    parser.add_argument('--eval_standard', type = str, default = "./data/spider2.0/spider2lite_eval.jsonl")
    parser.add_argument('--db_path', type = str, default = "./data/spider2.0/databases")

    args = parser.parse_args()

    evaluate(args.mode, args.gold_result_dir, args.eval_standard, args.gold, args.pred, args.db_path)
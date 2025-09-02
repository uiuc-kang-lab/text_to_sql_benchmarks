import sys
import sqlite3
import json
import argparse
import os
from tqdm import tqdm
import multiprocessing as mp
import random

random.seed(42)

execution_results = None
evaluation_results = None

def parse_option():
    parser = argparse.ArgumentParser()
    parser.add_argument('--pred', type = str, default = "predict_dev.json")
    parser.add_argument('--gold', type = str, default = "./bird/dev/dev.json")
    parser.add_argument('--db_path', type = str, default = "./bird/dev/dev_databases")
    parser.add_argument('--mode', type = str, default = "greedy_search")

    opt = parser.parse_args()

    return opt

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
        return data_idx, db_file, sql, execution_res, 1
    except:
        conn.rollback()
        conn.close()
        return data_idx, db_file, sql, None, 0

def compare_sql(question_id, db_file, question, ground_truth, pred_sql) :
    conn = sqlite3.connect(db_file)
    cursor = conn.cursor()
    correctness = 0

    try:
        conn.execute("BEGIN TRANSACTION;")
        cursor.execute(pred_sql)
        predicted_res = cursor.fetchall()
        cursor.execute(ground_truth)
        ground_truth_res = cursor.fetchall()
        print(f'[{question_id}] Successfully executed')
        if set(predicted_res) == set(ground_truth_res):
            correctness = 1
        else:
            print(f'predicted {len(predicted_res)}, ground_truth {len(ground_truth_res)}')
            print("predicted_res:", predicted_res)
            print("ground_truth_res:", ground_truth_res)
        conn.rollback()
    except:
        conn.rollback()
    finally:
        conn.close()
    return question_id, db_file, question, ground_truth, pred_sql, correctness

def run_evaluation(question_id, db_file, question, ground_truth, pred_sql):
    '''Run the evaluation for a single question'''
    try:
        result = compare_sql(question_id, db_file, question, ground_truth, pred_sql)
    except KeyboardInterrupt:
        sys.exit(0)
    except Exception as e:
        print(64, e)
        result = (question_id, db_file, question, ground_truth, pred_sql, 0)
    return result


def run_eval(gold_file, pred_file, db_path, mode, save_pred_sqls, num_cpus=1, timeout=100):
    evaluation_results = []
    gold = json.load(open(gold_file))
    pred_results = json.load(open(pred_file))
    question_ids = list(pred_results.keys())
    question_ids_int = [int(q_id) for q_id in question_ids]
    question_ids_int.sort()
    question_ids = [str(q_id) for q_id in question_ids_int]
    
    questions = []
    pred_sqls = [pred_results[str(i)] for i in question_ids]
    db_files = []
    ground_truth_sqls = []
    for data in gold:
        if str(data['question_id']) not in question_ids:
            continue
        ground_truth_sqls.append(data["SQL"]) 
        db_files.append(os.path.join(db_path, data["db_id"], data["db_id"] + ".sqlite"))
        questions.append(data["question"])
    print(len(question_ids), len(db_files), len(questions), len(ground_truth_sqls), len(pred_sqls))
    correctness_count = 0
    for question_id, db_file, question, ground_truth, pred_sql in tqdm(zip(question_ids, db_files, questions, ground_truth_sqls, pred_sqls), total=len(ground_truth_sqls)):
        try:
            result = run_evaluation(question_id, db_file, question, ground_truth, pred_sql)
            evaluation_results.append({
                "question_id": result[0],
                "db_file": result[1],
                "question": result[2],
                "ground_truth": result[3],
                "pred_sql": result[4],
                "correctness": result[5]
            })
            correctness_count += result[5]
            with open('results.txt', 'a') as f:
                f.write(f'{result[0]}\t{result[5]}\n')
        except KeyboardInterrupt:
            sys.exit(0)
        except Exception as e:
            print(42, e)
            evaluation_results.append({
                "question_id": question_id,
                "db_file": db_file,
                "question": question,
                "ground_truth": ground_truth,
                "pred_sql": pred_sql,
                "correctness": 0
            })
            with open('results.txt', 'a') as f:
                f.write(f'{result[0]}\t0\n')

    print(correctness_count)


if __name__ == "__main__":
    opt = parse_option()
    run_eval(opt.gold, opt.pred, opt.db_path, opt.mode, False)
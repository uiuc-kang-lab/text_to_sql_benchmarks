import os
import sqlite3
import json
import copy
import argparse
from configs.config import dev_databases_path, dev_json_path


def get_tables_and_columns(sqlite_db_path):
    with sqlite3.connect(sqlite_db_path) as conn:
        cursor = conn.cursor()
        tables = cursor.execute("SELECT name FROM sqlite_master WHERE type='table';").fetchall()

        return [
            f"{_table[0]}.{_column[1]}"
            for _table in tables
            for _column in cursor.execute(f"PRAGMA table_info('{_table[0]}');").fetchall()
        ]


def return_db_schema():
    # 读取所有数据库
    db_base_path = dev_databases_path
    db_schema = {}
    for db_name in os.listdir(db_base_path):
        db_path = os.path.join(db_base_path, db_name, db_name + '.sqlite')
        if os.path.exists(db_path):
            db_schema[db_name] = get_tables_and_columns(db_path)
    return db_schema


def extract_from_hint(output_path):
    db_schema_copy = copy.deepcopy(return_db_schema())
    with open(dev_json_path, 'r') as f:
        dev_set = json.load(f)

    pred_truths = []
    for i in range(len(dev_set)):
        hint = dev_set[i]['evidence']
        db_name = dev_set[i]['db_id']
        pred_truth = []
        list_db = [item.lower() for item in db_schema_copy[db_name]]
        for item in list_db:
            table = item.split('.')[0]
            if table == 'sqlite_sequence':
                continue
            column = item.split('.')[1]
            if column in hint.lower():
                pred_truth.append(item)

        pred_truths.append(pred_truth)

    tables = []
    for i in range(len(pred_truths)):
        table = []
        pred_truths[i] = [item.replace('.', '.`') + '`' for item in pred_truths[i]]
        for item in pred_truths[i]:
            t = item.split('.')[0]
            if t not in table:
                table.append(t)
        tables.append(table)

    answers = []
    for i in range(len(pred_truths)):
        answer = {}
        answer['tables'] = tables[i]
        answer['columns'] = pred_truths[i]
        answers.append(answer)

    with open(output_path, 'w') as f:
        json.dump(answers, f, indent=4, ensure_ascii=False)


def extract_from_sql(sql_file, output_file):
    db_schema_copy = copy.deepcopy(return_db_schema())
    with open(dev_json_path, 'r') as f:
        dev_set = json.load(f)

    with open(sql_file, 'r') as f:
        clms = f.readlines()

    pred_truths = []
    for i in range(len(clms)):
        clm = clms[i]
        db_name = dev_set[i]['db_id']

        pred_truth = []
        sql = clm.lower()
        list_db = [item.lower() for item in db_schema_copy[db_name]]
        for item in list_db:
            table = item.split('.')[0]
            if table == 'sqlite_sequence':
                continue
            column = item.split('.')[1]
            if column in sql:
                pred_truth.append(item)

        pred_truths.append(pred_truth)

    tables = []
    for i in range(len(pred_truths)):
        table = []
        pred_truths[i] = [item.replace('.', '.`') + '`' for item in pred_truths[i]]
        for item in pred_truths[i]:
            t = item.split('.')[0]
            if t not in table:
                table.append(t)
        tables.append(table)

    answers = []
    for i in range(len(pred_truths)):
        answer = {}
        answer['tables'] = tables[i]
        answer['columns'] = pred_truths[i]
        answers.append(answer)

    with open(output_file, 'w') as f:
        json.dump(answers, f, indent=4, ensure_ascii=False)


def merge(sql_file, LLM_file, hint_file, output_file):
    with open(sql_file, 'r') as f:
        clms = json.load(f)

    with open(LLM_file, 'r') as f:
        dev_set = json.load(f)

    with open(hint_file, 'r') as f:
        hint = json.load(f)

    answers = []

    for x, y, z in zip(clms, dev_set, hint):
        answer = {}

        tables = y['tables'] + x['tables'] + z['tables']
        columns = y['columns'] + x['columns'] + z['columns']
        tables = [item.lower() for item in tables]
        columns = [item.lower() for item in columns]

        tables = list(set(tables))
        columns = list(set(columns))

        answer['tables'] = tables
        answer['columns'] = columns
        answers.append(answer)

    with open(output_file, 'w') as f:
        json.dump(answers, f, indent=4, ensure_ascii=False)


def filter(dev_file, schema_file, output_file):
    db_schema_copy = copy.deepcopy(return_db_schema())

    with open(dev_file, 'r') as f:
        dev_set = json.load(f)

    with open(schema_file, 'r') as f:
        informations = json.load(f)

    preds = []
    for i in range(len(informations)):

        pred = []

        information = informations[i]
        db = dev_set[i]['db_id']

        db_schema = db_schema_copy[db]

        db_schema = [obj.replace('`', '') for obj in db_schema]

        columns = information['columns']
        columns = [obj.replace('`', '').lower() for obj in columns]

        for obj in db_schema:
            if obj.lower() in columns and obj.lower() not in pred:
                pred.append(obj)

        preds.append(pred)

    tables = []
    for i in range(len(preds)):
        table = []
        preds[i] = [item.replace('.', '.`') + '`' for item in preds[i]]
        for item in preds[i]:
            t = item.split('.')[0]
            if t not in table:
                table.append(t)
        tables.append(table)

    answers = []
    for i in range(len(preds)):
        answer = {}
        answer['tables'] = tables[i]
        answer['columns'] = preds[i]
        answers.append(answer)

    with open(output_file, 'w') as f:
        json.dump(answers, f, indent=4, ensure_ascii=False)


if __name__ == '__main__':
    # 创建 ArgumentParser 对象
    parser = argparse.ArgumentParser()

    # 添加命令行选项

    ## 这里的dataset是ppl_dev.json
    parser.add_argument("--pre_sql_file", type=str, default="src/sql_log/preliminary_sql.txt")
    parser.add_argument("--sql_sl_output", type=str, default="src/schema_linking/sql.json")
    parser.add_argument("--hint_sl_output", type=str, default="src/schema_linking/hint.json")
    parser.add_argument("--LLM_sl_output", type=str, default="src/schema_linking/LLM.json")

    parser.add_argument("--Schema_linking_output", type=str, default="src/schema_linking/schema.json")
    # 解析命令行参数
    args = parser.parse_args()

    extract_from_sql(args.pre_sql_file, args.sql_sl_output)
    extract_from_hint(args.hint_sl_output)
    merge(args.sql_sl_output, args.LLM_sl_output, args.hint_sl_output, args.Schema_linking_output)
    filter(dev_json_path, args.Schema_linking_output, args.Schema_linking_output)

import json
import os
import random
import re
import sqlite3
import traceback
from collections import defaultdict, OrderedDict
from pathlib import Path
from typing import List, Dict, Any

from func_timeout import FunctionTimedOut, func_timeout
from tqdm.contrib.concurrent import process_map

from cscsql.utils.constant import Constants
from cscsql.utils.file_utils import FileUtils
from cscsql.utils.logger_utils import logger
from cscsql.utils.chess_sql_parser import ChessSchemaParser
from cscsql.utils.sqlite_db_utils import SqliteDbUtils
from cscsql.utils.match_utils import MatchUtils

SPECIAL_SEPERATOR = "\t----- SQL-EVAL -----\t"
SPECIAL_SEPERATOR_BIRD = "\t----- bird -----\t"


def extract_xml_answer(text: str) -> str:
    answer = text.split("<answer>")[-1]
    answer = answer.split("</answer>")[0]
    return answer.strip()


def extract_sql(gen: str):
    gen = gen.replace("\n", " ")
    gen = gen.replace(";", "")
    gen = gen.replace("</s>", "")
    gen = gen.replace("```sql ", "")
    gen = gen.strip().replace("```", "")
    # cut from  the first SELECT
    if gen.find("</think>") > -1:
        gen = gen[gen.find("</think>") + len("</think>"):]

    gen = extract_xml_answer(gen)

    gen = gen.replace("</answer>", "")
    gen = gen.replace("<answer>", "")
    # select_index = gen.find("SELECT")
    # select_index = gen.rfind("SELECT")
    # gen = gen[select_index:]

    return gen


def parse_response(response: str, mode="sql"):
    result = response
    if mode == "sql":
        result = parse_response_for_sql(response)
    elif mode == "table":
        result = parse_response_for_table(response)
    else:
        result = parse_response_for_selection(response)
    return result


def parse_response_for_sql(response: str):
    if response.find("<answer>") > -1 and response.find("</answer>") > -1:
        # print("No SQL blocks found.")
        sql = extract_sql(response)
        if sql:
            return sql
        return ""
    else:
        pattern = r"```sql\s*(.*?)\s*```"

        sql_blocks = re.findall(pattern, response, re.DOTALL)

        if sql_blocks:
            # Extract the last SQL query in the response text and remove extra whitespace characters
            last_sql = sql_blocks[-1].strip()
            return last_sql
        else:
            sql = extract_sql(response)
            if sql:
                return sql
            return ""


def parse_response_for_selection(response: str):
    sql = extract_sql(response)
    result = MatchUtils.extract_sql_selection_result(sql)
    return result


def parse_response_for_table(response: str):
    sql = extract_sql(response)
    predicted_tables = sql.split(",")
    result = [item.strip() for item in predicted_tables if len(item.strip()) > 0]

    return result


def read_packed_sql(file: str, db_root: str):
    sqls, db_files = [], []

    db_id_list = []
    if file.endswith(".json"):
        raw_data = FileUtils.load_json(file)
        dev_file = db_root.replace("_databases", ".json")
        dev_data = FileUtils.load_json(dev_file)
        db_id_list = [item["db_id"] for item in dev_data]
    else:
        raw_data = FileUtils.read_to_text_list(file)
    for index, line in enumerate(raw_data):
        if isinstance(line, dict):
            db_id = line["db_id"]
            sql = line.get("SQL", line.get("query", ""))
        else:
            line = line.rstrip()
            if not line:
                continue

            sep = SPECIAL_SEPERATOR
            if line.find(SPECIAL_SEPERATOR_BIRD) > -1:
                sep = SPECIAL_SEPERATOR_BIRD
            elif line.find(SPECIAL_SEPERATOR) > -1:
                sep = SPECIAL_SEPERATOR
            elif line.find("\t") > -1:
                sep = "\t"
            one = line.split(sep)
            if len(one) == 2:
                sql, db_id = one[0], one[1]
            else:
                sql = line.strip()
                db_id = db_id_list[index]

        sqls.append(sql)
        db_file = Path(db_root).joinpath(db_id).joinpath(f"{db_id}.sqlite").resolve()
        db_files.append(str(db_file))

    print(f"Load {len(sqls)} SQLs from {file}")
    return sqls, db_files


def execute_sql(db_file, gen_sql, gold_sql, cmp_method="spider"):
    with sqlite3.connect(db_file) as conn:
        cursor = conn.cursor()

        cursor.execute(gen_sql)
        predicted_res = cursor.fetchall()

        res = predicted_res

    return res


def execute_model(packed):
    q_id, db_file, gen_sql, gold_sql, exec_time_out, mode = packed

    status = "failed"
    detail = None

    db_name = os.path.basename(db_file)
    db_id, end = os.path.splitext(db_name)
    try:
        res = func_timeout(exec_time_out, execute_sql, args=(db_file, gen_sql, gold_sql, mode))
        status = "success"
    except FunctionTimedOut:
        status = "timeout"
        res = f"execute sql timeout. "
    except Exception as e:
        detail = find_detail(str(e))
        status = "error"
        res = f"execute sql error message: {detail[:300]}"

    result = {"id": q_id, "db_id": db_id, "sql": gen_sql, "res": res, "status": status, "detail": detail}
    return result


def find_detail(reason):
    patterns = [
        "ambiguous column name",
        "no such column",
        "no such table",
        "no such function",
        "syntax error",
    ]

    for p in patterns:
        if p in reason:
            return p
    return "others"


def run_sqls_parallel(packed_payload, mode, num_workers=64, exec_time_out=30.0):
    ret = process_map(
        execute_model,
        [(*payload, exec_time_out, mode) for payload in packed_payload],
        max_workers=num_workers,
        chunksize=10,
    )
    return ret


class CommonUtils(object):

    @staticmethod
    def sorted_dict(label_dict, key=lambda x: x[1], reverse=True):
        """
        对词典进行排序
        :param label_dict:
        :param key:
        :param reverse:
        :return:
        """
        sort_list = sorted(label_dict.items(), key=key, reverse=reverse)
        sort_dict = OrderedDict()
        for row in sort_list:
            sort_dict[row[0]] = row[1]
        return sort_dict

    @staticmethod
    def read_link_table(link_table_files: str, is_train=False) -> List:
        link_table_results = None
        if link_table_files is None or link_table_files in ['none']:
            return link_table_results

        gen_table_file_list = link_table_files.split(",")
        raw_predicts = defaultdict(list)

        is_link_column = True if len(link_table_files) < 20 else False

        for file_name in gen_table_file_list:
            print(f"load link table file name: {file_name}")

            raw_data = FileUtils.load_json(file_name)
            for index, item in enumerate(raw_data):
                if is_link_column:
                    tables = item["tentative_schema"]
                elif "pred_sqls" in item:
                    pred_sqls = item["pred_sqls"]
                    raw_predict_tables = []
                    for gen in pred_sqls:
                        raw_predict_tables.extend(gen)
                    tables = list(set(raw_predict_tables))
                else:
                    tables = item["predicted_tables"]
                raw_predicts[index].append(tables)

        predicts = {}
        for index, pred_tables in raw_predicts.items():
            if is_link_column:
                tentative_schema = defaultdict(list)
                for schema in pred_tables:
                    for k, v in schema.items():
                        tentative_schema[k].extend(v)

                merge_schema = {}
                for k, v in tentative_schema.items():
                    merge_schema[k] = list(set(v))
                predicts[index] = merge_schema
            else:
                tables = []
                for table in pred_tables:
                    tables.extend(table)

                predicts[index] = list(set(tables))

        predict_sort = CommonUtils.sorted_dict(predicts, key=lambda x: int(x[0]), reverse=False)
        link_table_results = []
        for k, v in predict_sort.items():
            link_table_results.append(v)

        return link_table_results

    @staticmethod
    def build_link_table_from_ddl(instruction: str, current_predict_tables: List[str],
                                  tentative_schema: Dict = None):
        result = instruction
        if tentative_schema is None and isinstance(current_predict_tables, dict):
            tentative_schema = current_predict_tables
            current_predict_tables = None

        if tentative_schema is not None:
            if current_predict_tables:
                for table in tentative_schema.keys():
                    if table not in current_predict_tables:
                        current_predict_tables.append(table)
            else:
                current_predict_tables = list(tentative_schema.keys())

        if current_predict_tables is None or len(current_predict_tables) < 1:
            return result

        try:
            begin_str = "Database Schema:"
            end_str = "This schema describes the database's structure,"
            table_split_str = "CREATE TABLE "

            predict_tables = [c.lower() for c in current_predict_tables]

            raw_schema_index = instruction.find(begin_str)
            fk_index = instruction.find(end_str)
            if raw_schema_index > 0 and fk_index > 0:
                schema_index = raw_schema_index + len(begin_str)
                begin = instruction[:schema_index]
                schema = instruction[schema_index:fk_index]
                end = instruction[fk_index:]

                table_schema_list = schema.split(table_split_str)
                need_schema_list = []

                need_schema_table_name = []
                for item in table_schema_list:
                    if item.find("(") > -1:
                        table = item.split("(")[0].strip()
                        if table.lower() in predict_tables:
                            need_schema_list.append(item)
                            need_schema_table_name.append(table)

                if tentative_schema:
                    tentative_schema_lower = {k.lower(): v for k, v in tentative_schema.items()}
                    link_need_schema_list = []
                    for table, schema in zip(need_schema_table_name, need_schema_list):
                        link_columns = tentative_schema_lower.get(table.lower(), [])
                        new_schema = schema
                        if len(link_columns) > 0:
                            new_schema = CommonUtils.build_schema_link_columns(schema, link_columns)
                        link_need_schema_list.append(new_schema)

                    need_schema_list = link_need_schema_list

                link_schema = table_split_str.join(need_schema_list)
                if len(need_schema_list) > 0:
                    link_schema = f"\n{table_split_str}{link_schema}"
                else:
                    link_schema = schema

                new_end = end

                new_instruction = f"{begin}{link_schema}{new_end}"
                result = new_instruction
        except Exception as e:
            pass
        return result

    @staticmethod
    def build_schema_link_columns(schema: str, need_columns: List[str] = None):
        result = schema
        try:
            link_columns = []
            columns = schema.split("\n")
            total = len(columns)

            need_columns_lower = [item.lower() for item in need_columns]
            for index, item in enumerate(columns):
                if index in [0, total - 1]:
                    link_columns.append(item)
                    continue
                if item.upper().find("PRIMARY KEY") > -1 or item.upper().find("FOREIGN KEY") > -1:
                    link_columns.append(item)
                    continue

                column_name = item.strip()
                if len(column_name) > 2 and column_name.find(',') > -1:
                    if column_name.startswith("`"):
                        end_index = column_name.strip("`").find("`")
                        column_name = column_name[1:end_index + 1].rstrip("`").rstrip()
                    else:
                        end_index = column_name.find(" ")
                        column_name = column_name[:end_index].rstrip()

                    if column_name.lower() in need_columns_lower:
                        link_columns.append(item)
                else:
                    link_columns.append(item)

            result = "\n".join(link_columns)
        except Exception as e:
            pass
        return result

    @staticmethod
    def build_revision_prompt(instruction: str, predict_result: Dict = None):
        result = instruction
        if predict_result is None:
            return result
        try:
            task_msg = "You are a data science expert. Below, you are provided with a database schema and a natural language question. Your task is to understand the schema and generate a valid SQL query to answer the question."
            new_task_msg = "You are a data science expert. Below, you are provided with a database schema, a natural language question, a draft SQL and its corresponding execution result. Your task is to understand the schema and revise the draft SQL. If the current SQL query is correct, return the query directly."

            new_instruction = instruction.replace(task_msg, new_task_msg)

            other_msg = "Instructions:"
            new_other_msg = "Instructions:"

            predict_sql = predict_result["sql"]
            execute_result = predict_result["res"]
            execute_result = CommonUtils.normal_execute_result(execute_result)
            # execute_status = predict_result["status"]
            new_revision_msg = f"""Predicted draft SQL: 
{predict_sql}

SQL execute result: 
{execute_result}

{new_other_msg}"""
            new_instruction = new_instruction.replace(other_msg, new_revision_msg)
            result = new_instruction
        except Exception as e:
            traceback.print_exc()
            pass

        return result

    @staticmethod
    def build_selection_vote_prompt(instruction: str, predict_result: Dict = None):
        result = instruction
        if predict_result is None:
            return result
        try:
            task_msg = "You are a data science expert. Below, you are provided with a database schema and a natural language question. Your task is to understand the schema and generate a valid SQL query to answer the question."
            new_task_msg = "You are a data science expert. Below, you are provided with a database schema, a natural language question, two candidate SQL and its corresponding execution result. Your task is to understand the schema and select the correct candidate SQL."

            new_instruction = instruction.replace(task_msg, new_task_msg)

            other_msg = "Instructions:"
            new_other_msg = "Instructions:"

            predict_sql = predict_result["sql1"]
            execute_result = predict_result["res1"]
            execute_result = CommonUtils.normal_execute_result(execute_result)

            predict_sql2 = predict_result["sql2"]
            execute_result2 = predict_result["res2"]
            execute_result2 = CommonUtils.normal_execute_result(execute_result2)

            new_selection_msg = f"""Predicted candidate SQL and execution result: 
Candidate A
{predict_sql}

Candidate A execute result: 
{execute_result}

****************

Candidate B
{predict_sql2}

Candidate B execute result: 
{execute_result2}


{new_other_msg}"""
            new_instruction = new_instruction.replace(other_msg, new_selection_msg)

            instruction_msg = """Instructions:\n- Make sure you only output the information that is asked in the question. If the question asks for a specific column, make sure to only include that column in the SELECT clause, nothing more.\n- The generated query should return all of the information asked in the question without any missing or extra information.\n- Before generating the final SQL query, please think through the steps of how to write the query."""

            # # - When users write the candidate SQL, they also fill in the confidence score. Please note that the confidence score only represents the user's initial evaluation of the current candidate and is for reference only. The confidence score of candidate A is 0.6, and the confidence score of candidate B is 0.4.
            instruction_msg2 = """Instructions:
- Remember that if none of the candidates are correct after analysis, then the first candidate is output."""

            # instruction_msg2 = ""
            new_instruction = new_instruction.replace(instruction_msg, instruction_msg2)

            current_predict_tables = CommonUtils.extract_target_table_names_from_sql([predict_sql, predict_sql2])
            new_instruction = CommonUtils.build_link_table_from_ddl(new_instruction, current_predict_tables)

            result = new_instruction
        except Exception as e:
            traceback.print_exc()
            pass

        return result

    @staticmethod
    def build_merge_generate_prompt(instruction: str, predict_result: Dict = None):
        result = instruction
        if predict_result is None:
            return result
        try:
            task_msg = "You are a data science expert. Below, you are provided with a database schema and a natural language question. Your task is to understand the schema and generate a valid SQL query to answer the question."
            new_task_msg = "You are a data science expert. Below, you are provided with a database schema, a natural language question, some draft SQL and its corresponding execution result. Your task is to understand the schema and generate a valid SQL query to answer the question."

            new_instruction = instruction.replace(task_msg, new_task_msg)

            other_msg = "Instructions:"
            new_other_msg = "Instructions:"

            predict_sql = predict_result["sql1"]
            execute_result = predict_result["res1"]
            execute_result = CommonUtils.normal_execute_result(execute_result)

            predict_sql2 = predict_result["sql2"]
            execute_result2 = predict_result["res2"]
            execute_result2 = CommonUtils.normal_execute_result(execute_result2)

            tentative_schema = predict_result['tentative_schema']
            link_tables = predict_result['link_tables']

            candidate_sql_msg = []
            need_sql = [predict_sql, predict_sql2]
            need_sql_result = [execute_result, execute_result2]
            for i, sql in enumerate(need_sql):
                sql_res = need_sql_result[i]
                if len(str(sql)) > 500:
                    sql = sql[:500]
                msg = f"{i + 1}. {sql}\n【Execution result】\n{sql_res}\n"
                candidate_sql_msg.append(msg)

            candidate_sql = "\n".join(candidate_sql_msg)
            new_selection_msg = f"""Here are some corresponding draft SQL and execute result: 
{candidate_sql}

{new_other_msg}"""
            new_instruction = new_instruction.replace(other_msg, new_selection_msg)

            # current_predict_tables = CommonUtils.extract_target_table_names_from_sql([predict_sql, predict_sql2])
            current_predict_tables = link_tables
            new_instruction = CommonUtils.build_link_table_from_ddl(new_instruction,
                                                                    current_predict_tables,
                                                                    tentative_schema=tentative_schema)

            result = new_instruction
        except Exception as e:
            traceback.print_exc()
            pass

        return result

    @staticmethod
    def extract_target_table_names_from_sql(sqls: List[str]):
        if isinstance(sqls, str):
            sqls = [sqls]

        results = []
        for sql in sqls:
            try:
                sql = sql.lower().replace("\n", " ")
                table_names = sql.split()
                results.extend(table_names)
            except Exception as e:
                pass
        results = list(set(results))
        return results

    @staticmethod
    def get_db_path(db_root: str, db_id: str):
        db_file = Path(db_root).joinpath(db_id).joinpath(f"{db_id}.sqlite").resolve()
        db_path = str(db_file)
        return db_path

    @staticmethod
    def get_all_db_full_schema_and_sample(db_root: str, sample_limit=3):
        all_db_ids = FileUtils.list_dir(db_root)
        db_full_schema_config = {}
        db_sample_config = defaultdict(dict)

        save_base = f"{db_root}"
        db_full_schema_config_file = f"{save_base}db_full_schema_config.json"
        db_sample_config_file = f"{save_base}db_sample_config.json"
        if os.path.exists(db_full_schema_config_file) and os.path.exists(db_sample_config_file):
            db_full_schema_config = FileUtils.load_json(db_full_schema_config_file)
            db_sample_config = FileUtils.load_json(db_sample_config_file)
            return db_full_schema_config, db_sample_config

        for db_id in all_db_ids:
            db_uri = CommonUtils.get_db_path(db_root=db_root, db_id=db_id)
            db_full_schema = SqliteDbUtils.get_db_table_and_columns(cursor=None, db_path=db_uri)
            db_full_schema_config[db_id] = db_full_schema

            cursor = SqliteDbUtils.get_cursor_from_path(db_uri)
            for table_name in db_full_schema.keys():
                sample_rows = SqliteDbUtils.get_table_sample_rows(cursor, table_name, sample_limit=sample_limit,
                                                                  db_uri=db_uri)
                db_sample_config[db_id][table_name] = sample_rows

        if not os.path.exists(db_full_schema_config_file):
            FileUtils.dump_json(db_full_schema_config_file, db_full_schema_config)

        if not os.path.exists(db_sample_config_file):
            FileUtils.dump_json(db_sample_config_file, db_sample_config)

        return db_full_schema_config, db_sample_config

    @staticmethod
    def aggregate_columns(columns_dicts: List[Dict[str, Any]], selected_tables: List[str],
                          merge_cot=False, question_id=None) -> Dict[str, List[str]]:
        """
        Aggregates columns from multiple responses and consolidates reasoning.

        Args:
            columns_dicts (List[Dict[str, Any]]): List of dictionaries containing column names and reasoning.
            selected_tables (List[str]): List of selected tables.

        Returns:
            Dict[str, List[str]]: Aggregated result with unique column names and consolidated reasoning.
        """
        question_id_msg = "" if question_id is None else f", question_id: {question_id}"
        # logger.info(f"Aggregating columns from multiple responses{question_id_msg}")
        columns = {}
        chain_of_thoughts = []
        for column_dict in columns_dicts:
            valid_column_dict = False
            dict_cot = None
            for key, value in column_dict.items():
                if key == "chain_of_thought_reasoning":
                    dict_cot = value
                else:  # key is table name
                    table_name = key
                    if table_name.startswith("`"):
                        table_name = table_name[1:-1]
                    column_names = value
                    if table_name.lower() in [t.lower() for t in selected_tables]:
                        for column_name in column_names:
                            if column_name.startswith("`"):
                                column_name = column_name[1:-1]
                            if table_name not in columns:
                                columns[table_name] = []
                            if column_name.lower() not in [col.lower() for col in columns[table_name]]:
                                columns[table_name].append(column_name)
                            valid_column_dict = True
            if valid_column_dict and dict_cot:
                chain_of_thoughts.append(dict_cot)

        aggregated_chain_of_thoughts = "\n----\n".join(chain_of_thoughts)
        aggregation_result = columns
        if merge_cot:
            aggregation_result["chain_of_thought_reasoning"] = aggregated_chain_of_thoughts

        # logger.info(f"Aggregated columns: {columns}")
        return aggregation_result

    @staticmethod
    def get_diff_merge_schema(full_schema: Dict, tentative_schema: Dict):
        normal_tentative_schema = {}
        link_tables = []
        link_column_names = []
        for table, val in tentative_schema.items():
            link_tables.append(table)

            current_table_columns = full_schema.get(table, full_schema.get(table.lower(), {}))
            target_dict = {}
            for c in current_table_columns:
                target_dict[c] = c
                target_dict[c.lower()] = c

            link_columns = []
            for name in list(val):
                if name in target_dict:
                    link_columns.append(target_dict[name])
                elif name.lower() in target_dict:
                    link_columns.append(target_dict[name.lower()])

            link_column_names.append(link_columns)
            normal_tentative_schema[table] = link_columns

        return link_column_names, link_tables, normal_tentative_schema

    @staticmethod
    def extract_merge_schema_from_sql(sqls: List, db_uri: str, db_full_schema: Dict, question_id=None):
        columns_dict_list = []
        all_run_sql = []
        for item in sqls:
            if isinstance(item, list):
                all_run_sql.extend(item)
            else:
                all_run_sql.append(item)
        for predict_sql in all_run_sql:
            columns_dict = ChessSchemaParser.get_sql_columns_dict(db_path=db_uri, sql=predict_sql)
            columns_dict_list.append(columns_dict)

        all_tables = SqliteDbUtils.get_db_all_tables(db_uri)
        tentative_schema = CommonUtils.aggregate_columns(columns_dict_list,
                                                         selected_tables=all_tables,
                                                         merge_cot=False,
                                                         question_id=question_id)

        link_column_names, link_tables, normal_tentative_schema = CommonUtils.get_diff_merge_schema(db_full_schema,
                                                                                                    tentative_schema)

        return link_column_names, link_tables, normal_tentative_schema

    @staticmethod
    def normal_execute_result(execute_result):
        if execute_result and isinstance(execute_result, list) and len(execute_result) > 20:
            need_item = execute_result[:20]
            if len(str(need_item)) > 1000:
                need_item = str(need_item)[:1000] + "...]"
            execute_result = f"The execution results of the first twenty columns are: {need_item}"
        if execute_result and len(str(execute_result)) > 1000:
            execute_result = str(execute_result)[:1000] + "..."
        return execute_result

    @staticmethod
    def get_few_shot_list(dataset_name: str = Constants.DATASET_NAME, file_type: str = Constants.DATASET_MODE) -> List[
        List[Dict]]:
        base_dir = f"{Constants.NLP_DATA_DIR}/{dataset_name}"
        eval_file_name = f"{base_dir}/{file_type}/{file_type}_same.csv"
        raw_contents = FileUtils.read_to_text_list(eval_file_name)

        train_file_name = f"{base_dir}/train/train.json"
        train_data = FileUtils.load_json(train_file_name)

        print(f"load few shot from {dataset_name} - {file_type} : {len(raw_contents)} -train data: {len(train_data)}")

        results = []
        for index, line in enumerate(raw_contents):
            all_index = line.split(",")
            idx = int(all_index[0])
            few_shot = all_index[1:]
            few_shot = [int(i) for i in few_shot]
            if index != idx:
                raise RuntimeError(f"few shot error: {eval_file_name} - {index} ！= {idx}")

            same_few_shots = [train_data[idx] for idx in few_shot]
            results.append(same_few_shots)

        return results

    @staticmethod
    def build_few_shot_example_msg(current_few_shot: List[Dict]):
        results = []
        for index, item in enumerate(current_few_shot):
            question = item["question"]
            query = item.get("SQL", item.get("query", ""))
            evidence = item.get("evidence", "")

            evidence_str = ""
            if evidence and len(evidence) > 0:
                evidence = evidence.replace("\n", " ")
                evidence_str = f"""{evidence}"""
                # evidence_str = f"""#External Knowledge: {evidence}\n"""

            template = f"""#Example Question: {evidence_str}\n{question}\n#Answer: `{query}`"""
            results.append(template)

        few_shot_str = "\n\n".join(results)
        few_shot_msg = f"Here are some reference examples:\n{few_shot_str}\n"
        return few_shot_msg

    @staticmethod
    def execute_batch_sql_to_result(gen_sqls_file: str, db_root: str,
                                    mode="bird",
                                    num_workers=32, exec_time_out=30.0):
        predict_sql_results = None
        try:
            gen_sqls, gen_dbs = read_packed_sql(gen_sqls_file, db_root=db_root)

            gold_ids = [index for index in range(len(gen_sqls))]
            packed_payload = zip(gold_ids, gen_dbs, gen_sqls, gen_sqls)

            exec_result = run_sqls_parallel(
                packed_payload,
                mode=mode,
                num_workers=num_workers,
                exec_time_out=exec_time_out,
            )

            predict_sql_results = {item["id"]: item for item in exec_result}
            predict_sql_results = CommonUtils.sorted_dict(predict_sql_results, key=lambda x: int(x[0]), reverse=False)

            print(f"execute sql: {len(predict_sql_results)} - {db_root} - {gen_sqls_file}")
        except Exception as e:
            traceback.print_exc()

        return predict_sql_results

    @staticmethod
    def execute_batch_vote_sql_to_result(selection_vote_file: str, db_root: str,
                                         is_train=False,
                                         prompt_mode="merge",
                                         mode="bird",
                                         num_workers=32, exec_time_out=30.0):
        vote_predict_sql_results = None
        all_predict_results = []
        try:
            if not selection_vote_file.endswith("_pred_major_top2_sqls.json"):
                selection_vote_file = selection_vote_file.replace(".json", "_pred_major_top2_sqls.json")

            raw_data = FileUtils.load_json(selection_vote_file)
            dev_file = db_root.replace("_databases", ".json")
            dev_data = FileUtils.load_json(dev_file)

            dev_data_config = {index: item for index, item in enumerate(dev_data)}

            gen_sqls = []
            gen_dbs = []
            gold_ids = []
            gen_sqls2 = []

            correctness = {}
            correctness1 = {}
            correctness2 = {}

            none_gold = 0
            for index, (item, dev_item) in enumerate(zip(raw_data, dev_data)):
                question_id = dev_item.get('question_id', index)
                db_id = dev_item["db_id"]
                sql = item['sql']
                correctness_list = item['correctness_list']
                sql_list = [sql] if isinstance(sql, str) else sql

                new_item = {
                    "id": question_id,
                    "db_id": db_id,
                    'correctness': correctness_list[0],
                    'sql': sql_list[0],
                }
                all_predict_results.append(new_item)
                if len(sql_list) < 2:
                    continue

                flag = True
                for s in sql_list:
                    if s is None or len(s.strip()) < 10 or not s.strip().lower().startswith("select"):
                        flag = False

                if not flag:
                    continue

                if is_train and item['correctness'] == 0:
                    gold = dev_data_config[question_id]['SQL']
                    item['correctness'] = 1

                    if random.choice([0, 1]) == 1:
                        sql_list = [sql_list[0], gold]
                        correctness_list = [0, 1]
                    else:
                        sql_list = [gold, sql_list[0]]
                        correctness_list = [1, 0]

                    none_gold += 1

                if is_train and prompt_mode in ['vote'] and item['correctness'] == 0:
                    continue

                db_file = Path(db_root).joinpath(db_id).joinpath(f"{db_id}.sqlite").resolve()
                gen_dbs.append(str(db_file))
                gold_ids.append(question_id)
                gen_sqls.append(sql_list[0])
                gen_sqls2.append(sql_list[1])

                correctness[question_id] = item['correctness']
                correctness1[question_id] = correctness_list[0]
                correctness2[question_id] = correctness_list[1]

            print(f"total diff vote sql: {len(gen_sqls)}")
            # gen_sqls, gen_dbs = read_packed_sql(gen_sqls_file, db_root=db_root)
            # gold_ids = [index for index in range(len(gen_sqls))]
            packed_payload = zip(gold_ids, gen_dbs, gen_sqls, gen_sqls)
            exec_result1 = run_sqls_parallel(
                packed_payload,
                mode=mode,
                num_workers=num_workers,
                exec_time_out=exec_time_out,
            )

            packed_payload2 = zip(gold_ids, gen_dbs, gen_sqls2, gen_sqls2)
            exec_result2 = run_sqls_parallel(
                packed_payload2,
                mode=mode,
                num_workers=num_workers,
                exec_time_out=exec_time_out,
            )

            predict_sql_results = {item["id"]: item for item in exec_result1}
            predict_sql_results = CommonUtils.sorted_dict(predict_sql_results, key=lambda x: int(x[0]), reverse=False)

            predict_sql_results2 = {item["id"]: item for item in exec_result2}
            predict_sql_results2 = CommonUtils.sorted_dict(predict_sql_results2, key=lambda x: int(x[0]), reverse=False)

            db_full_schema_config, db_sample_config = CommonUtils.get_all_db_full_schema_and_sample(db_root=db_root)

            vote_predict_sql_results = {}
            for question_id, item in predict_sql_results.items():
                item2 = predict_sql_results2.get(question_id, item)

                db_id = item['db_id']
                db_uri = CommonUtils.get_db_path(db_root=db_root, db_id=db_id)
                db_full_schema = db_full_schema_config[db_id]

                link_column_names, link_tables, normal_tentative_schema = CommonUtils.extract_merge_schema_from_sql(
                    sqls=[item['sql'], item2['sql']],
                    db_uri=db_uri,
                    db_full_schema=db_full_schema,
                    question_id=question_id)

                new_item = {
                    "id": item['id'],
                    "db_id": item['db_id'],
                    "vote_top2_correctness": correctness.get(question_id, 0),
                    "sql1": item['sql'],
                    "res1": item['res'],
                    "status1": item['status'],
                    "detail1": item['detail'],
                    "sql1_correctness": correctness1.get(question_id, 0),
                    "sql2": item2['sql'],
                    "res2": item2['res'],
                    "status2": item2['status'],
                    "detail2": item2['detail'],
                    "sql2_correctness": correctness2.get(question_id, 0),
                    "tentative_schema": normal_tentative_schema,
                    "link_tables": link_tables,
                }

                vote_predict_sql_results[question_id] = new_item

            vote_predict_sql_results = CommonUtils.sorted_dict(vote_predict_sql_results, key=lambda x: int(x[0]),
                                                               reverse=False)

            print(f"diff vote execute sql: {len(vote_predict_sql_results)} - {db_root} - {selection_vote_file}")
            print(f"none gold: {none_gold} - {none_gold / len(vote_predict_sql_results)}")
        except Exception as e:
            traceback.print_exc()

        return vote_predict_sql_results, all_predict_results

    @staticmethod
    def major_vote_for_sql(pred_file, db_path, mode, save_pred_sqls, num_cpus=30, timeout=30):
        pass

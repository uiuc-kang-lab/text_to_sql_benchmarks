import json
import sqlite3
import os
import sys
import re
import time

from tqdm import tqdm
from func_timeout import func_timeout, FunctionTimedOut
import multiprocessing as mp
import ijson

def execute_sql(sql, db_path):
    if sql.strip() == "":
        return None

    execution_result = None
    column_count = None
    conn = None
    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()

        # start a transaction
        cursor.execute("BEGIN")

        # execute the SQL query
        cursor.execute(sql)
        execution_result = cursor.fetchall()
        column_count = len(cursor.description)
        
        # roll back the transaction to ensure that the database state is not changed
        cursor.execute("ROLLBACK")
    except Exception as e:
        # print(f"An error occurred: {e}")
        pass
    finally:
        if conn is not None:
            conn.close()
    return execution_result, column_count

def execute_wrapper(sample_idx, db_id, sql, complexity, timeout, db_dir):
    try:
        execution_result, column_count = func_timeout(timeout, execute_sql, args = (sql, os.path.join(db_dir, db_id, db_id + ".sqlite")))
        if execution_result is None or column_count is None:
            return [sample_idx, db_id, sql, complexity, 0, 0, 0]
        else:
            return [sample_idx, db_id, sql, complexity, 1, column_count, len(execution_result)]
    except KeyboardInterrupt:
        sys.exit(0)
    except FunctionTimedOut:
        return [sample_idx, db_id, sql, complexity, 0, 0, 0]
    except Exception as e:
        return [sample_idx, db_id, sql, complexity, 0, 0, 0]

def execute_callback(result):
    sample_idx, db_id, sql, complexity, valid_flag, column_count, rows = result
    if valid_flag == 1:
        no_timeout_synthesized_sqls.append(
            {"db_id": db_id, "sql": sql, "column_count": column_count, "rows": rows, "complexity": complexity}
        )
    # print("Done:", sample_idx)

def remove_timeout_sqls_parallel(synthesized_sqls, db_dir, num_cpus = 20, timeout = 1):
    '''Execute the sqls in parallel'''
    parallel_batch_size = 10240
    batches = [synthesized_sqls[i: i+parallel_batch_size] for i in range(0, len(synthesized_sqls), parallel_batch_size)]

    assert len(synthesized_sqls) == sum([len(batch_sqls) for batch_sqls in batches])

    for batch_idx, batch_sqls in enumerate(batches):
        print(f"execution process: {batch_idx+1}/{len(batches)}")
        pool = mp.Pool(processes = num_cpus)
        for sample_idx, sql_info in enumerate(batch_sqls):
            pool.apply_async(
                execute_wrapper, 
                args = (sample_idx, sql_info["db_id"], sql_info["sql"], sql_info["complexity"], timeout, db_dir), 
                callback = execute_callback
            )
        pool.close()
        pool.join()
        time.sleep(10)

def analyze_complexity(results):
    complexity2num = dict()
    for res in results:
        complexity = res["complexity"]
        if complexity in complexity2num:
            complexity2num[complexity] += 1
        else:
            complexity2num[complexity] = 1
    print(complexity2num)

def analyze_column_count(results):
    column_count2num = dict()
    for res in results:
        column_count = res["column_count"]
        if column_count in column_count2num:
            column_count2num[column_count] += 1
        else:
            column_count2num[column_count] = 1
    print(column_count2num)

def analyze_advanced_functions(results):
    function2num = dict()
    functions = json.load(open("prompt_templates/sqlite_funcs.json"))
    functions = [func_desc.split("(")[0] for func_desc in functions]

    for res in results:
        sql = res["sql"]
        for function in functions:
            if function.lower()+"(" in sql.lower():
                if function in function2num:
                    function2num[function] += 1
                else:
                    function2num[function] = 1

    print(function2num)

def analyze_used_tables_num(synthesized_sqls, db_id2table_names):
    used_tables_num2count = dict()
    for sql_info in tqdm(synthesized_sqls):
        table_names_in_db = db_id2table_names[sql_info["db_id"]]
        sql = sql_info["sql"]
        if sql.endswith(";"):
            sql = sql[:-1]
        sql_tokens = sql.strip().lower().split()
        # print(table_names_in_db)
        # print(sql_tokens)

        used_tables = set()

        for table_name in table_names_in_db:
            if table_name.lower() in sql_tokens:
                used_tables.add(table_name.lower())

        used_tables_num = len(used_tables)
        # print(used_tables)
        # print(used_tables_num)
        # print("------------------------------------------")
        if used_tables_num in used_tables_num2count:
            used_tables_num2count[used_tables_num] += 1
        else:
            used_tables_num2count[used_tables_num] = 1
    
    print(used_tables_num2count)


def filter_executable_sqls(synthesized_sqls, db_dir):
    executable_sqls = []
    for sql_info in tqdm(synthesized_sqls):
        db_path = os.path.join(db_dir, sql_info["db_id"], sql_info["db_id"] + ".sqlite")
        query_plan, _ = execute_sql("EXPLAIN QUERY PLAN " + sql_info["sql"], db_path)
        if query_plan is not None:
            sql_info["query_plan"] = str(query_plan)
            executable_sqls.append(sql_info)
    return executable_sqls

def filter_select_sqls(synthesized_sqls):
    '''
        remain SELECT-type queries
    '''
    select_sqls = []
    for sql_info in tqdm(synthesized_sqls):
        # remove comments
        sql_wo_comments = re.sub(r'/\*.*?\*/', '', sql_info["sql"], flags=re.DOTALL)
        sql_wo_comments = re.sub(r'--.*', '', sql_wo_comments)
        sql_wo_comments = sql_wo_comments.strip()

        if sql_wo_comments.lower().startswith("select") or \
            sql_wo_comments.lower().startswith("with"):
            select_sqls.append(sql_info)
    return select_sqls

def dedup_using_query_plan(synthesized_sqls):
    unique_plans = set()
    deduped_sqls = []
    for sql_info in tqdm(synthesized_sqls):
        query_plan = sql_info["query_plan"]
        if query_plan not in unique_plans:
            unique_plans.add(query_plan)
            deduped_sqls.append(sql_info)
    return deduped_sqls

def obtain_sql_template(sql):
    # Handles single and double quoted strings, numbers, NULL, TRUE, FALSE
    pattern = r"""
        (?<!\w)'(?:\\.|[^'])*' |  # single quoted strings
        (?<!\w)"(?:\\.|[^"])*" |  # double quoted strings
        (?<!\w)-?\b\d+(\.\d+)?([eE][-+]?\d+)?\b | # numbers with scientific notation
        \bNULL\b |                # NULL
        \bTRUE\b |                # TRUE
        \bFALSE\b                 # FALSE
    """

    # replace values with a special token <value>
    template = re.sub(pattern, "<value>", sql, flags=re.IGNORECASE | re.VERBOSE)
    template = template.lower().replace("\n", " ").strip()
    
    # Replace multiple spaces with a single space
    template = re.sub(r'\s+', ' ', template)
    
    return template

def dedup_using_query_template(synthesized_sqls):
    unique_templates = set()
    deduped_sqls = []
    for sql_info in tqdm(synthesized_sqls):
        template = obtain_sql_template(sql_info["sql"])
        if template not in unique_templates:
            unique_templates.add(template)
            deduped_sqls.append(sql_info)
    return deduped_sqls

def parse_response(response):
    pattern = r"```sql\s*(.*?)\s*```"
    
    sql_blocks = re.findall(pattern, response, re.DOTALL)

    if sql_blocks:
        # Extract the last SQL query in the response text and remove extra whitespace characters
        last_sql = sql_blocks[-1].strip()
        return last_sql
    else:
        # print("No SQL blocks found.")
        return ""

def obtain_db_id2table_names(results, db_dir):
    db_ids = list(set([res["db_id"] for res in results]))
    print("len(db_ids):", len(db_ids))
    db_id2table_names = dict()
    for db_id in db_ids:
        results, _ = execute_sql(
            "SELECT name FROM sqlite_master WHERE type='table';", 
            os.path.join(db_dir, db_id, db_id + ".sqlite")
        )
        table_names = [res[0] for res in results]
        db_id2table_names[db_id] = table_names
    return db_id2table_names

def load_json_file(file):
    dataset = []
    with open(file, 'r', encoding='utf-8') as f:
        objects = ijson.items(f, 'item')
        for obj in tqdm(objects):
            dataset.append(obj)
    return dataset

if __name__ == "__main__":
    synthesized_sqls = []
    db_dir = "../database_synthesis/synthetic_sqlite_databases"
    llm_responses = load_json_file("./results/sql_synthesis.json")
    
    for llm_response in tqdm(llm_responses):
        sql = parse_response(llm_response["response"])
        if sql == "":
            continue
        synthesized_sqls.append(
            {
                "db_id": llm_response["db_id"][:-3] if llm_response["db_id"].endswith(".db") else llm_response["db_id"], 
                "sql": sql,
                "complexity": llm_response["prompt"].split("Ensure the SQL query matches the ")[1].split(" level, defined as follows:")[0]
            }
        )

    print("original sql num:", len(synthesized_sqls))
    # analyze_complexity(synthesized_sqls)
    # analyze_advanced_functions(synthesized_sqls)

    # remove non-SELECT sqls
    synthesized_sqls = filter_select_sqls(synthesized_sqls)
    print("sql num after removing non-SELECT sql queries:", len(synthesized_sqls))
    # analyze_complexity(synthesized_sqls)
    # analyze_advanced_functions(synthesized_sqls)
    
    # remove sqls with syntax errors
    synthesized_sqls = filter_executable_sqls(synthesized_sqls, db_dir)
    print("sql num after removing syntax-error sqls:", len(synthesized_sqls))
    # analyze_complexity(synthesized_sqls)
    # analyze_advanced_functions(synthesized_sqls)

    # # perform deduplication according to the query plan
    # synthesized_sqls = dedup_using_query_plan(synthesized_sqls)
    # print("sql num after deduplication (query plan level):", len(synthesized_sqls))
    # print(synthesized_sqls[0].keys())
    # # analyze_complexity(synthesized_sqls)
    # # analyze_advanced_functions(synthesized_sqls)

    # remove timeout sqls
    no_timeout_synthesized_sqls = mp.Manager().list()
    remove_timeout_sqls_parallel(synthesized_sqls, db_dir, 10, 2)
    synthesized_sqls = list(no_timeout_synthesized_sqls)
    print("sql num after removing timeout sqls:", len(synthesized_sqls))
    print(synthesized_sqls[0].keys())
    # analyze_complexity(synthesized_sqls)
    analyze_column_count(synthesized_sqls)
    # analyze_advanced_functions(synthesized_sqls)

    # perform deduplication according to the query template
    synthesized_sqls = dedup_using_query_template(synthesized_sqls)
    print("sql num after deduplication (tempalte level):", len(synthesized_sqls))
    # analyze_complexity(synthesized_sqls)
    analyze_column_count(synthesized_sqls)
    # analyze_advanced_functions(synthesized_sqls)

    # analyze the number of used tables
    analyze_used_tables_num(
        synthesized_sqls, 
        obtain_db_id2table_names(synthesized_sqls, db_dir)
    )

    with open("./results/synthetic_sqls.json", "w", encoding="utf-8") as f:
        f.write(json.dumps(synthesized_sqls, indent=2, ensure_ascii=False))
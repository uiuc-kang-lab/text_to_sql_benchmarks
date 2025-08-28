import json
import os
import re
import random
import ast
import operator
import sqlite3
from collections import defaultdict
import time
from itertools import product
from pathlib import Path
from typing import List, Tuple, Set, Dict

from func_timeout import FunctionTimedOut, func_timeout
from tqdm.contrib.concurrent import process_map

from cscsql.utils.common_utils import CommonUtils
from cscsql.utils.constant import Constants


def load_json(filename) -> json:
    if not os.path.exists(filename):
        return dict()

    with open(filename, 'r', encoding='utf8') as f:
        return json.load(f)


def format_reward(completions, **kwargs):
    """Reward function that checks if the reasoning process is enclosed within <think> and </think> tags, while the final answer is enclosed within <answer> and </answer> tags."""
    pattern = r"^<think>\n.*?\n</think>\n<answer>\n.*?\n</answer>$"
    completion_contents = [completion[0]["content"] for completion in completions]
    matches = [re.match(pattern, content, re.DOTALL | re.MULTILINE) for content in completion_contents]
    return [1.0 if match else 0.0 for match in matches]


def now_str(time_format="%Y-%m-%d %H:%M:%S"):
    return time.strftime(time_format, time.localtime())


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


def extract_json(gen: str):
    gen = gen.replace("\n", " ")
    gen = gen.replace(";", "")
    gen = gen.replace("</s>", "")
    gen = gen.replace("}}", "}")

    pattern = r"```json\s*(.*?)\s*```"
    json_blocks = re.findall(pattern, gen, re.DOTALL)

    result = None
    if json_blocks:
        last_raw_json = json_blocks[-1].strip()
        try:
            result = json.loads(last_raw_json)
        except Exception as e:
            pass
            # traceback.print_exc()
            # logger.info(f"error extract json: {gen}")

    if result is None:
        gen = gen.replace("```json ", "")
        gen = gen.strip().replace("```", "")
        gen = gen.strip().replace("json", "")
        gen = gen.strip().replace('"""', "")
        raw_json = extract_sql(gen)
        try:
            raw_json = raw_json.strip().rstrip()
            if raw_json.find("{") < 0:
                raw_json = '{' + raw_json
            if raw_json.find("}") < 0:
                raw_json = raw_json + "}"

            result = json.loads(raw_json)
        except Exception as e:
            pass
            # traceback.print_exc()
            # print(f"error extract json: {raw_json} -\n {gen}")

    if result is None:
        result = {}

    return result


def extract_xml_answer(text: str) -> str:
    answer = text.split("<answer>")[-1]
    answer = answer.split("</answer>")[0]
    return answer.strip()


def extract_sql_selection_result(predict: str):
    result = None
    try:
        predict = predict.strip()
        if len(predict) == 1:
            result = predict[0]
        elif len(predict) > 1:
            if predict.upper().startswith("A"):
                result = "A"
            elif predict.upper().startswith("B"):
                result = "B"

        if result is not None:
            result = result.upper()
    except Exception as e:
        print(f"extract_sql_selection_result error: {predict} - {result}")
        result = None
    return result


def extract_solution(solution_str: str):
    """Extract the equation from the solution string."""
    # Remove everything before the first "Assistant:"

    final_answer = None

    solution_str = solution_str.replace("\n", " ")
    pattern = r"<think>.*</think>.*<answer>.*</answer>"
    if not re.match(pattern, solution_str):
        return final_answer

    final_answer = extract_xml_answer(solution_str)
    final_answer = extract_sql(final_answer)
    return final_answer


def get_predict_columns_from_schema(predicts: Dict[str, List[str]]) -> List:
    predict_columns = []
    if not isinstance(predicts, dict):
        return predicts
    for k, vals in predicts.items():
        if isinstance(vals, list):
            for v in vals:
                item = f"`{k}`.`{v}`"
                predict_columns.append(item.lower())
    return predict_columns


def permute_tuple(element: Tuple, perm: Tuple) -> Tuple:
    assert len(element) == len(perm)
    return tuple([element[i] for i in perm])


def unorder_row(row: Tuple) -> Tuple:
    return tuple(sorted(row, key=lambda x: str(x) + str(type(x))))


# unorder each row in the table
# [result_1 and result_2 has the same bag of unordered row]
# is a necessary condition of
# [result_1 and result_2 are equivalent in denotation]
def quick_rej(result1: List[Tuple], result2: List[Tuple], order_matters: bool) -> bool:
    s1 = [unorder_row(row) for row in result1]
    s2 = [unorder_row(row) for row in result2]
    if order_matters:
        return s1 == s2
    else:
        return set(s1) == set(s2)


# return whether two bag of relations are equivalent
def multiset_eq(l1: List, l2: List) -> bool:
    if len(l1) != len(l2):
        return False
    d = defaultdict(int)
    for e in l1:
        d[e] = d[e] + 1
    for e in l2:
        d[e] = d[e] - 1
        if d[e] < 0:
            return False
    return True


def get_constraint_permutation(tab1_sets_by_columns: List[Set], result2: List[Tuple]):
    num_cols = len(result2[0])
    perm_constraints = [{i for i in range(num_cols)} for _ in range(num_cols)]
    if num_cols <= 3:
        return product(*perm_constraints)

    # we sample 20 rows and constrain the space of permutations
    for _ in range(20):
        random_tab2_row = random.choice(result2)

        for tab1_col in range(num_cols):
            for tab2_col in set(perm_constraints[tab1_col]):
                if random_tab2_row[tab2_col] not in tab1_sets_by_columns[tab1_col]:
                    perm_constraints[tab1_col].remove(tab2_col)
    return product(*perm_constraints)


# check whether two denotations are correct
def result_eq(result1: List[Tuple], result2: List[Tuple], order_matters: bool) -> bool:
    if len(result1) == 0 and len(result2) == 0:
        return True

    # if length is not the same, then they are definitely different bag of rows
    if len(result1) != len(result2):
        return False

    num_cols = len(result1[0])

    # if the results do not have the same number of columns, they are different
    if len(result2[0]) != num_cols:
        return False

    # unorder each row and compare whether the denotation is the same
    # this can already find most pair of denotations that are different
    if not quick_rej(result1, result2, order_matters):
        return False

    # the rest of the problem is in fact more complicated than one might think
    # we want to find a permutation of column order and a permutation of row order,
    # s.t. result_1 is the same as result_2
    # we return true if we can find such column & row permutations
    # and false if we cannot
    tab1_sets_by_columns = [{row[i] for row in result1} for i in range(num_cols)]

    # on a high level, we enumerate all possible column permutations that might make result_1 == result_2
    # we decrease the size of the column permutation space by the function get_constraint_permutation
    # if one of the permutation make result_1, result_2 equivalent, then they are equivalent
    for perm in get_constraint_permutation(tab1_sets_by_columns, result2):
        if len(perm) != len(set(perm)):
            continue
        if num_cols == 1:
            result2_perm = result2
        else:
            result2_perm = [permute_tuple(element, perm) for element in result2]
        if order_matters:
            if result1 == result2_perm:
                return True
        else:
            # in fact the first condition must hold if the second condition holds
            # but the first is way more efficient implementation-wise
            # and we use it to quickly reject impossible candidates
            if set(result1) == set(result2_perm) and multiset_eq(result1, result2_perm):
                return True
    return False


def execute_sql(db_file, gen_sql, gold_sql, cmp_method="spider"):
    with sqlite3.connect(db_file) as conn:
        cursor = conn.cursor()

        cursor.execute(gen_sql)
        predicted_res = cursor.fetchall()

        cursor.execute(gold_sql)
        ground_truth_res = cursor.fetchall()

        res = 0
        if cmp_method == "spider":
            order_matters = "orderby" in re.sub(r"\s+", gold_sql.lower(), "")
            if result_eq(predicted_res, ground_truth_res, order_matters=order_matters):
                res = 1
        elif cmp_method == "bird":
            if set(predicted_res) == set(ground_truth_res):
                res = 1

    return res


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


def execute_model(packed):
    q_id, db_file, gen_sql, gold_sql, exec_time_out, mode = packed

    status = "failed"
    detail = None
    try:
        res = func_timeout(exec_time_out, execute_sql, args=(db_file, gen_sql, gold_sql, mode))
        status = "success"
    except FunctionTimedOut:
        status = "timeout"
        res = 0
    except Exception as e:
        detail = find_detail(str(e))
        status = "error"
        res = 0

    result = {"id": q_id, "res": res, "status": status, "detail": detail}
    return result


def validate_predict_sql(predict_sql: str, db_id: str, question_id, gold_sql: str,
                         exec_time_out=30.0, dataset_name="bird", split="dev", ):
    """Validate that equation only uses available numbers and each number once."""
    try:
        db_split = split
        db_root = f"{Constants.DATASET_DIR}/{dataset_name}/{db_split}/{db_split}_databases"
        db_file = Path(db_root).joinpath(db_id).joinpath(f"{db_id}.sqlite").resolve()
        db_file = str(db_file)

        packed = [question_id, db_file, predict_sql, gold_sql, exec_time_out, dataset_name]
        result = execute_model(packed)
        equal_flag = result["res"]

        return equal_flag == 1
    except:
        return False


def evaluate_equation(equation_str):
    """Safely evaluate the arithmetic equation using eval() with precautions."""
    try:
        # Define a regex pattern that only allows numbers, operators, parentheses, and whitespace
        allowed_pattern = r'^[\d+\-*/().\s]+$'
        if not re.match(allowed_pattern, equation_str):
            raise ValueError("Invalid characters in equation.")

        # Evaluate the equation with restricted globals and locals
        result = eval(equation_str, {"__builtins__": None}, {})
        return result
    except Exception as e:
        return None


def compute_score(solution_str, ground_truth, method='strict', format_score=0.1, score=1., **kwargs):
    """The scoring function for countdown task.

    Args:
        solution_str: the solution text
        ground_truth: dictionary containing target number and available numbers
        method: the method to extract the solution
        format_score: the score for correct format but wrong answer
        score: the score for the correct answer
    """

    dataset_name = ground_truth.get('dataset_name', "bird")
    split = ground_truth['split']
    question_id = ground_truth['question_id']
    db_id = ground_truth['db_id']
    gold_sql = ground_truth['sql']

    predict_sql = extract_solution(solution_str=solution_str)
    do_print = random.randint(1, 64) == 1

    if predict_sql is None:
        if do_print:
            current_time = now_str()
            print(f"--------------------------------")
            print(
                f"{current_time} - No sql found, Question_id: {question_id} | db_id: {db_id} | Solution string: {solution_str}")
        return 0

    if dataset_name == "bird" and split == "test":
        split = "dev"

    flag = validate_predict_sql(predict_sql, question_id=question_id,
                                db_id=db_id, gold_sql=gold_sql,
                                dataset_name=dataset_name,
                                split=split, )

    if do_print:
        current_time = now_str()
        print(f"--------------------------------")
        print(f"{current_time} - Question_id: {question_id} | db_id: {db_id}")
        print(f"Predict sql correct: {flag}")
        print(f"Gold sql: {gold_sql}")
        print(f"Extracted sql: {predict_sql}")
        print(f"Solution string: {solution_str}")

    # Validate sql uses gold sql
    if flag:
        return score
    else:
        if do_print:
            print(f"Invalid SQL !!!")

        return format_score


def run_sqls_parallel(packed_payload, mode, num_workers=64, exec_time_out=30.0):
    ret = process_map(
        execute_model,
        [(*payload, exec_time_out, mode) for payload in packed_payload],
        max_workers=num_workers,
        chunksize=10,
    )
    return ret


def execute_accuracy_reward(completions, ground_truth, method='strict', format_score=0.1, score=1.,
                            num_workers=64, exec_time_out=30.0, **kwargs):
    """The scoring function for countdown task.

    Args:
        completions: the solution text
        ground_truth: dictionary containing target number and available numbers
        method: the method to extract the solution
        format_score: the score for correct format but wrong answer
        score: the score for the correct answer
    """
    contents = [completion[0]["content"] for completion in completions]

    run_dataset_name = ground_truth[0].get('dataset_name', "bird")

    predict_sqls = []
    gold_sqls = []
    db_path_list = []
    question_ids = []

    db_id_list = []

    for content, target in zip(contents, ground_truth):
        predict_sql = extract_sql(content)

        predict_sqls.append(predict_sql)

        dataset_name = target.get('dataset_name', "bird")
        db_split = target.get('split', 'dev')
        question_id = target['question_id']
        db_id = target['db_id']
        gold_sql = target['sql']

        db_root = f"{Constants.DATASET_DIR}/{dataset_name}/{db_split}/{db_split}_databases"
        db_file = Path(db_root).joinpath(db_id).joinpath(f"{db_id}.sqlite").resolve()
        db_file = str(db_file)

        question_ids.append(question_id)
        db_id_list.append(db_id)
        db_path_list.append(db_file)
        gold_sqls.append(gold_sql)

    packed_payload = zip(question_ids, db_path_list, predict_sqls, gold_sqls)

    exec_result = run_sqls_parallel(
        packed_payload,
        mode=run_dataset_name,
        num_workers=num_workers,
        exec_time_out=exec_time_out,
    )

    rewards = [score if res["res"] == 1 else 0 for res in exec_result]

    do_print = random.randint(1, 64) == 1

    if do_print:
        current_time = now_str()

        print(f"--------------------------------")
        print(f"{current_time} - Question_id: {question_ids[0]} | db_id: {db_id_list[0]}")
        print(f"Predict sql correct: {rewards[0]}")
        print(f"Gold sql: {gold_sqls[0]}")
        print(f"Extracted sql: {predict_sqls[0]}")
        print(f"Solution string: {contents[0]}")
        if rewards[0] == 0:
            print(f"Invalid SQL !!!")

    return rewards


def selection_vote_reward(completions, ground_truth, method='strict', format_score=0.1, score=1.,
                          num_workers=64, exec_time_out=30.0, **kwargs):
    """The scoring function for countdown task.

    Args:
        completions: the solution text
        ground_truth: dictionary containing target number and available numbers
        method: the method to extract the solution
        format_score: the score for correct format but wrong answer
        score: the score for the correct answer
    """
    contents = [completion[0]["content"] for completion in completions]

    one = ground_truth[0]

    predict_sqls = []
    rewards = []
    for content, target in zip(contents, ground_truth):
        predict_sql = extract_sql(content)
        predict_sql = extract_sql_selection_result(predict_sql)

        predict_sqls.append(predict_sql)

        dataset_name = target.get('dataset_name', "bird")
        db_split = target.get('split', 'dev')
        question_id = target['question_id']
        db_id = target['db_id']
        gold_sql = target['sql']

        if predict_sql is not None \
                and str(predict_sql).strip().lower() == gold_sql.strip().lower():
            rewards.append(score)
        else:
            rewards.append(0)

    do_print = random.randint(1, 64) == 1

    if do_print:
        current_time = now_str()

        print(f"--------------------------------")
        print(f"{current_time} - Question_id: {one['question_id']} | db_id: {one['db_id']}")
        print(f"Predict sql correct: {rewards[0]}")
        print(f"Gold sql: {one['sql']}")
        print(f"Extracted sql: {predict_sqls[0]}")
        print(f"Solution string: {contents[0]}")
        if rewards[0] == 0:
            print(f"Invalid vote !!!")

    return rewards


def link_table_reward(completions, ground_truth, method='strict', format_score=0.1, score=1.,
                      num_workers=64, exec_time_out=30.0, **kwargs):
    """The scoring function for countdown task.

    Args:
        completions: the solution text
        ground_truth: dictionary containing target number and available numbers
        method: the method to extract the solution
        format_score: the score for correct format but wrong answer
        score: the score for the correct answer
    """
    contents = [completion[0]["content"] for completion in completions]

    one = ground_truth[0]

    predict_sqls = []
    rewards = []
    for content, target in zip(contents, ground_truth):
        predict_sql = extract_sql(content)
        predict_sql = [item.strip() for item in predict_sql.split(",")]

        predict_sqls.append(predict_sql)

        dataset_name = target.get('dataset_name', "bird")
        db_split = target.get('split', 'dev')
        question_id = target['question_id']
        db_id = target['db_id']
        gold_sql = target['sql']

        predicted_tables = [x.lower().strip() for x in predict_sql]
        reference_tables = [x.lower().strip() for x in gold_sql]

        # Calculate accuracy
        acc_flag = False
        if set(predicted_tables) == set(reference_tables):
            acc_flag = True

        # Calculate precision and recall
        true_positives = len(set(predicted_tables) & set(reference_tables))
        false_positives = len(set(predicted_tables) - set(reference_tables))
        false_negatives = len(set(reference_tables) - set(predicted_tables))

        filter_acc_flag = False
        if true_positives == len(reference_tables):
            filter_acc_flag = True

        if acc_flag:
            rewards.append(score)
        elif filter_acc_flag:
            rewards.append(0.5)
        else:
            rewards.append(0)

    do_print = random.randint(1, 64) == 1

    if do_print:
        current_time = now_str()

        print(f"--------------------------------")
        print(f"{current_time} - Question_id: {one['question_id']} | db_id: {one['db_id']}")
        print(f"Predict link table correct: {rewards[0]}")
        print(f"Gold link table: {one['sql']}")
        print(f"Extracted link table: {predict_sqls[0]}")
        print(f"Solution string: {contents[0]}")
        if rewards[0] == 0:
            print(f"Invalid link table !!!")

    return rewards


def link_column_reward(completions, ground_truth, method='strict', format_score=0.1, score=1.,
                       num_workers=64, exec_time_out=30.0, **kwargs):
    """The scoring function for countdown task.

    Args:
        completions: the solution text
        ground_truth: dictionary containing target number and available numbers
        method: the method to extract the solution
        format_score: the score for correct format but wrong answer
        score: the score for the correct answer
    """
    contents = [completion[0]["content"] for completion in completions]

    one = ground_truth[0]

    predict_sqls = []
    rewards = []
    for content, target in zip(contents, ground_truth):
        predict_sql = extract_json(content)

        predict_sqls.append(predict_sql)

        dataset_name = target.get('dataset_name', "bird")
        db_split = target.get('split', 'dev')
        question_id = target['question_id']
        db_id = target['db_id']
        gold_sql = target['sql']

        predicted_tables = get_predict_columns_from_schema(predict_sql)
        reference_tables = get_predict_columns_from_schema(gold_sql)

        # Calculate accuracy
        acc_flag = False
        if set(predicted_tables) == set(reference_tables):
            acc_flag = True

        # Calculate precision and recall
        true_positives = len(set(predicted_tables) & set(reference_tables))
        false_positives = len(set(predicted_tables) - set(reference_tables))
        false_negatives = len(set(reference_tables) - set(predicted_tables))

        filter_acc_flag = False
        if true_positives == len(reference_tables):
            filter_acc_flag = True

        if acc_flag:
            rewards.append(score)
        elif filter_acc_flag:
            rewards.append(0.5)
        else:
            rewards.append(0)

    do_print = random.randint(1, 64) == 1

    if do_print:
        current_time = now_str()

        print(f"--------------------------------")
        print(f"{current_time} - Question_id: {one['question_id']} | db_id: {one['db_id']}")
        print(f"Predict link column correct: {rewards[0]}")
        print(f"Gold link column: {one['sql']}")
        print(f"Extracted link column: {predict_sqls[0]}")
        print(f"Solution string: {contents[0]}")
        if rewards[0] == 0:
            print(f"Invalid link column !!!")

    return rewards


def link_column_from_sql_reward(completions, ground_truth, method='strict', format_score=0.1, score=1.,
                       num_workers=64, exec_time_out=30.0, **kwargs):
    """The scoring function for countdown task.

    Args:
        completions: the solution text
        ground_truth: dictionary containing target number and available numbers
        method: the method to extract the solution
        format_score: the score for correct format but wrong answer
        score: the score for the correct answer
    """
    contents = [completion[0]["content"] for completion in completions]

    one = ground_truth[0]


    predict_sqls = []
    rewards = []
    for content, target in zip(contents, ground_truth):
        predict_sql = extract_sql(content)

        predict_sqls.append(predict_sql)

        dataset_name = target.get('dataset_name', "bird")
        db_split = target.get('split', 'train')
        question_id = target['question_id']
        db_id = target['db_id']
        gold_sql = target['sql']

        if db_split == "dev":
            db_root = Constants.SQL_DATASET_DIR_DEV
            db_full_schema_config, db_sample_config = CommonUtils.get_all_db_full_schema_and_sample(db_root=db_root)
            db_uri = CommonUtils.get_db_path(db_root=db_root, db_id=db_id)
            db_full_schema = db_full_schema_config[db_id]
        else:
            db_root = Constants.SQL_DATASET_DIR_TRAIN
            db_full_schema_config, db_sample_config = CommonUtils.get_all_db_full_schema_and_sample(db_root=db_root)
            db_uri = CommonUtils.get_db_path(db_root=db_root, db_id=db_id)
            db_full_schema = db_full_schema_config[db_id]

        link_column_names, link_tables, normal_tentative_schema = CommonUtils.extract_merge_schema_from_sql(
            sqls=[predict_sql],
            db_uri=db_uri,
            db_full_schema=db_full_schema,
            question_id=question_id)

        gold_link_column_names, gold_link_tables, gold_normal_tentative_schema = CommonUtils.extract_merge_schema_from_sql(
            sqls=[gold_sql],
            db_uri=db_uri,
            db_full_schema=db_full_schema,
            question_id=question_id)

        # link table
        predicted_tables = [x.lower().strip() for x in link_tables]
        reference_tables = [x.lower().strip() for x in gold_link_tables]

        table_acc_flag = False
        if set(predicted_tables) == set(reference_tables):
            table_acc_flag = True

        # Calculate precision and recall
        table_true_positives = len(set(predicted_tables) & set(reference_tables))
        table_false_positives = len(set(predicted_tables) - set(reference_tables))
        table_false_negatives = len(set(reference_tables) - set(predicted_tables))

        table_filter_acc_flag = False
        if table_true_positives == len(reference_tables):
            table_filter_acc_flag = True

        # link column
        predicted_columns = get_predict_columns_from_schema(normal_tentative_schema)
        reference_columns = get_predict_columns_from_schema(gold_normal_tentative_schema)

        column_acc_flag = False
        if set(predicted_columns) == set(reference_columns):
            column_acc_flag = True

        # Calculate precision and recall
        column_true_positives = len(set(predicted_columns) & set(reference_columns))
        column_false_positives = len(set(predicted_columns) - set(reference_columns))
        column_false_negatives = len(set(reference_columns) - set(predicted_columns))

        column_filter_acc_flag = False
        if column_true_positives == len(reference_columns):
            column_filter_acc_flag = True

        if column_acc_flag:
            rewards.append(score)
        elif column_filter_acc_flag:
            rewards.append(0.7)
        elif table_acc_flag:
            rewards.append(0.4)
        elif table_filter_acc_flag:
            rewards.append(0.2)
        else:
            rewards.append(0)

    do_print = random.randint(1, 100) == 1

    if do_print:
        current_time = now_str()

        print(f"--------------------------------")
        print(f"{current_time} - Question_id: {one['question_id']} | db_id: {one['db_id']}")
        print(f"Predict link column correct: {rewards[0]}")
        print(f"Gold link column: {one['sql']}")
        print(f"Extracted link column: {predict_sqls[0]}")
        print(f"Solution string: {contents[0]}")
        if rewards[0] == 0:
            print(f"Invalid link column !!!")

    return rewards

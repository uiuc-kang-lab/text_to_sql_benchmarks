from llm.Binary_GPT import GPT
import json
from tqdm import tqdm
from utils.util import execute_sql
from utils.simplified_schema import simplified, explanation_collection
import argparse


def prompt_construct(simple_ddl, ddl_data, foreign_key, explanation, ppl, sql1, sql2):
    db = ppl['db']
    question = ppl['question'].strip()
    evidence = ppl['evidence'].strip()
    example = ppl['example']

    table_info = '### Sqlite SQL tables, with their properties:\n'
    table_info += simple_ddl + '\n' + '### Here are some data information about database references.\n' + ddl_data + '\n### Foreign key information of Sqlite SQL tables, used for table joins:\n' + foreign_key + '\n### The meaning of every column:\n#\n' + explanation.strip() + "\n#\n"

    table_info = example.strip() + '\n\n' + "### Answer the question by sqlite SQL query only and with no explanation. You must minimize SQL execution time while ensuring correctness.\n" + table_info.strip() + '\n\n' + '### definition: ' + evidence + "\n### Question: " + question

    r1, c1, re1 = execute_sql(sql1, db)
    r2, c2, re2 = execute_sql(sql2, db)

    candidate_sql = f"### sql1: {sql1} \n### result1: {re1} \n### sql2: {sql2} \n### result2: {re2}"

    return table_info, candidate_sql


def sql_generation(table_info, candidate_sql):
    binary_gpt = GPT()
    answer = binary_gpt(table_info, candidate_sql)
    try:
        answer = json.loads(answer)
    except Exception as e:
        print(e)
        answer = answer.replace("\\", "\\\\")
        answer = json.loads(answer)
    return answer


def main(ppl_file, output_file, sql_file1, sql_file2, x=0):
    # 1.加载prompt信息 从0开始
    with open(ppl_file, 'r') as f:
        ppls = json.load(f)

    with open(sql_file1, 'r') as f:
        sqls1s = f.readlines()

    with open(sql_file2, 'r') as f:
        sqls2s = f.readlines()

    answers = []

    for i in tqdm(range(x, len(ppls))):
        ppl = ppls[i]
        sql1 = sqls1s[i].strip()
        sql2 = sqls2s[i].strip()

        # 简化ddl
        simple_ddl, ddl_data, foreign_key = simplified(ppl)

        # 列描述
        explanation = explanation_collection(ppl)

        table_info, candidate_sql = prompt_construct(simple_ddl, ddl_data, foreign_key, explanation, ppl, sql1, sql2)

        # 3.4. thought_gpt
        sql = sql_generation(table_info, candidate_sql)
        answer = sql['sql'].replace('\n', ' ')
        answers.append(answer)

        with open(output_file, 'w', encoding='utf-8') as file:
            for sql in answers:
                file.write(str(sql) + '\n')


if __name__ == '__main__':
    # 创建 ArgumentParser 对象
    parser = argparse.ArgumentParser()

    # 添加命令行选项

    parser.add_argument("--start_index", type=int, default=0)
    parser.add_argument("--ppl_file", type=str, default="src/information/ppl_dev.json")
    parser.add_argument("--sql_3_output", type=str, default="src/sql_log/step_3_binary.txt")
    parser.add_argument("--sql_1", type=str, default="src/sql_log/preliminary_sql.txt")
    parser.add_argument("--sql_2", type=str, default="src/sql_log/step_2_information_augmentation.txt")

    # 解析命令行参数
    args = parser.parse_args()

    main(args.ppl_file, args.sql_3_output, args.sql_1, args.sql_2, args.start_index)

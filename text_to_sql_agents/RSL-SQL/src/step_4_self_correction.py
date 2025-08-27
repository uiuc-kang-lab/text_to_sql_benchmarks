from llm.self_correction_gpt import GPT
import json
from tqdm import tqdm
from utils.util import execute_sql
from configs.Instruction import SELF_CORRECTION_PROMPT
from utils.simplified_schema import simplified, explanation_collection
import argparse


def table_info_construct(ppl, simple_ddl, ddl_data, foreign_key, explanation):
    question = ppl['question'].strip()
    evidence = ppl['evidence'].strip()
    example = ppl['example']

    table_info = '### Sqlite SQL tables, with their properties:\n'
    table_info += simple_ddl + '\n' + '### Here are some data information about database references.\n' + ddl_data + '\n### Foreign key information of Sqlite SQL tables, used for table joins:\n' + foreign_key + '\n### The meaning of every column:\n#\n' + explanation.strip() + "\n#\n"

    table_info += f'\n### sql_keywords: {ppl["sql_keywords"]}'
    table_info += f'\n### conditions: {ppl["conditions"]}'

    table_info = example.strip() + '\n\n' + "### Answer the question by sqlite SQL query only and with no explanation. You must minimize SQL execution time while ensuring correctness.\n" + table_info.strip() + '\n\n' + '### Hint: ' + evidence + "\n### Question: " + question + '\n\n' + 'The hint aims to direct your focus towards the specific elements of the database schema that are crucial for answering the question effectively.'

    return table_info


def main(ppl_file, sql_file, output_file, x=0):
    gpt = GPT()

    # 1.加载prompt信息 从0开始
    with open(ppl_file, 'r') as f:
        ppls = json.load(f)

    with open(sql_file, 'r') as f:
        pre_sqls = f.readlines()

    sys_message = SELF_CORRECTION_PROMPT

    answers = []

    for i in tqdm(range(x, len(ppls))):
        message = []
        message.append({'role': 'system', 'content': sys_message})
        ppl = ppls[i]
        db = ppl['db']

        # 简化ddl
        simple_ddl, ddl_data, foreign_key = simplified(ppl)

        # 列描述
        explanation = explanation_collection(ppl)

        table_info = table_info_construct(ppl, simple_ddl, ddl_data, foreign_key, explanation)

        pre_sql = pre_sqls[i].strip()

        num = 0
        while num < 5:

            row_count, column_count, result = execute_sql(pre_sql, db)

            if num > 0:
                table_info = "### Buggy SQL: " + pre_sql.strip() + "\n" + f"### The result of the buggy SQL is [{result.strip()}]. Please fix the SQL to get the correct result."
            if row_count == 0 and column_count == 0:
                message.append({'role': 'user', 'content': table_info})
                message, answer = gpt(message)
                num += 1
                try:
                    answer = json.loads(answer)
                except Exception as e:
                    answer = answer.replace('\\', '\\\\')
                    try:
                        answer = json.loads(answer)
                    except Exception as e:
                        break
                pre_sql = answer['sql'].strip()
            else:
                break
        answers.append(pre_sql.replace('\n', ' '))
        with open(output_file, 'w') as f:
            for answer in answers:
                f.write(answer + '\n')


if __name__ == '__main__':
    # 创建 ArgumentParser 对象
    parser = argparse.ArgumentParser()

    # 添加命令行选项

    parser.add_argument("--start_index", type=int, default=0)
    parser.add_argument("--ppl_file", type=str, default="src/information/ppl_dev.json")
    parser.add_argument("--sql_4_output", type=str, default="src/sql_log/final_sql.txt")
    parser.add_argument("--sql_refinement", type=str, default="src/sql_log/step_3_binary.txt")

    # 解析命令行参数
    args = parser.parse_args()

    main(args.ppl_file, args.sql_refinement, args.sql_4_output, args.start_index)

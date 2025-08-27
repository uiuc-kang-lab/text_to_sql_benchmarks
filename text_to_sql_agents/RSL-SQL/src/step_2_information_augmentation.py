from llm.LLM import GPT as model
import json
from tqdm import tqdm
from utils.simplified_schema import simplified, explanation_collection
from configs.Instruction import TABLE_AUG_INSTRUCTION, KEY_WORD_AUG_INSTRUCTION, CONDITION_AUG_INSTRUCTION, \
    SQL_GENERATION_INSTRUCTION
import argparse


def table_info_construct(simple_ddl, ddl_data, foreign_key, explanation):
    table_info = ('### Sqlite SQL tables, with their properties:\n' + simple_ddl +
                  '\n### Here are some data information about database references.\n' + ddl_data +
                  '\n### Foreign key information of Sqlite SQL tables, used for table joins:\n' + foreign_key +
                  '\n### The meaning of every column:\n#\n' + explanation.strip() +
                  '\n#\n')

    return table_info


def table_augmentation(table_info, ppl):
    question = ppl['question'].strip()
    evidence = ppl['evidence'].strip()

    gpt = model()
    table_gpt_res_prompt = table_info.strip() + '\n\n' + '### definition: ' + evidence + "\n### Question: " + question
    table_gpt_res = gpt(TABLE_AUG_INSTRUCTION, table_gpt_res_prompt)
    table_gpt_res = json.loads(table_gpt_res)
    return table_gpt_res


def key_word_augmentation(table_info, ppl):
    gpt = model()

    question = ppl['question'].strip()
    evidence = ppl['evidence'].strip()
    word_gpt_res_prompt = table_info.strip() + '\n\n' + '### definition: ' + evidence + "\n### Question: " + question
    word_gpt_res = gpt(KEY_WORD_AUG_INSTRUCTION, word_gpt_res_prompt)

    word_gpt_res = json.loads(word_gpt_res)
    return word_gpt_res


def condition_augmentation(ppl):
    gpt = model()

    question = ppl['question'].strip()
    relation_gpt_res = gpt(CONDITION_AUG_INSTRUCTION, question)
    relation_gpt_res = json.loads(relation_gpt_res)
    return relation_gpt_res


def sql_generation(ppl, table_aug, word_aug, cond_aug, table_info):
    gpt = model()

    question = ppl['question'].strip()
    evidence = ppl['evidence'].strip()
    example = ppl['example']
    table_info += f'\n### sql_keywords: {word_aug["sql_keywords"]}\n'
    table_info += f'### tables: {table_aug["tables"]}\n'
    table_info += f'### columns: {table_aug["columns"]}\n'
    table_info += f'### conditions: {cond_aug["conditions"]}'

    table_info = example.strip() + '\n\n' + "### Answer the question by sqlite SQL query only and with no explanation. You must minimize SQL execution time while ensuring correctness.\n" + table_info.strip() + '\n\n' + '### definition: ' + evidence + "\n### Question: " + question

    # 3.4. thought_gpt
    answer = gpt(SQL_GENERATION_INSTRUCTION, table_info)
    try:
        answer = json.loads(answer)
    except Exception as e:
        print(e)
        answer = answer.replace("\\", "\\\\")
        answer = json.loads(answer)
    sql = answer['sql'].replace('\n', ' ')
    return sql


def main(ppl_file, output_file, info_file, x):
    # 1.加载prompt信息 从0开始
    with open(ppl_file, 'r') as f:
        ppls = json.load(f)

    answers = []
    informations = []

    for i in tqdm(range(x, len(ppls))):
        information = {}
        ppl = ppls[i]

        # 简化ddl
        simple_ddl, ddl_data, foreign_key = simplified(ppl)

        # 列描述
        explanation = explanation_collection(ppl)

        # table_info
        table_info = table_info_construct(simple_ddl, ddl_data, foreign_key, explanation)

        # table_aug
        table_aug = table_augmentation(table_info, ppl)
        information['tables'] = table_aug['tables']
        information['columns'] = table_aug['columns']

        # word_aug
        word_aug = key_word_augmentation(table_info, ppl)
        information['sql_keywords'] = word_aug['sql_keywords']

        # condition_aug
        cond_aug = condition_augmentation(ppl)
        information['conditions'] = cond_aug['conditions']
        informations.append(information)

        # sql_generation
        sql = sql_generation(ppl, table_aug, word_aug, cond_aug, table_info)

        answers.append(sql)

        with open(output_file, 'w', encoding='utf-8') as file:
            for sql in answers:
                file.write(str(sql) + '\n')
        with open(info_file, 'w', encoding='utf-8') as file:
            json.dump(informations, file, indent=4, ensure_ascii=False)


if __name__ == '__main__':
    # 创建 ArgumentParser 对象
    parser = argparse.ArgumentParser()

    # 添加命令行选项

    parser.add_argument("--start_index", type=int, default=0)
    parser.add_argument("--ppl_file", type=str, default="src/information/ppl_dev.json")
    parser.add_argument("--sql_2_output", type=str, default="src/sql_log/step_2_information_augmentation.txt")
    parser.add_argument("--information_output", type=str, default="src/information/augmentation.json")
    # 解析命令行参数
    args = parser.parse_args()

    main(args.ppl_file, args.sql_2_output, args.information_output, args.start_index)

import copy
import json
import os
import re
import sys
from itertools import islice
from tqdm import tqdm
from openai import OpenAI

project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(project_root)
from tools.sql_executor import value_example_extractor, one_sql_execute, value_example_extractor_masked_extra_schema
from tools.extractor import text_extractor
from tools.format_masked_regenerate_schema import transform_data_predict_symbol_column_description_hint
from run_config import API_KEYS, model_openai, SQL_FORMAT_PROMPT, SQL_EXECUTE_OUTPUT_CORRECT_PROMPT, SQL_EXECUTE_OUTPUT_CORRECT_PROMPT_CHECK_OUTPUT_back_part_1, SQL_EXECUTE_OUTPUT_CORRECT_PROMPT_CHECK_OUTPUT_back_part_2


client = OpenAI(
    api_key=API_KEYS)

def extract_sql_query(input_string):
    match = re.search(r'###\s*SQL:\s*(.*)###\s*END', input_string)
    if match:
        return match.group(1)
    return None

def extract_schema_info(input_string):
    pattern = r'###\s*Related Schema(.*?)###\s*END'

    match = re.search(pattern, input_string, re.DOTALL)
    if match:

        related_schema_content = match.group(1).strip()

        #print(related_schema_content)

        table_pattern = r'Table (\w+):\s*columns:([^}]+)'
        schema_list = re.findall(table_pattern, related_schema_content)


        table_dict = {}

        for item in schema_list:
            table_name = item[0]

            columns_pattern = r'"([^"]+)"'
            table_columns = re.findall(columns_pattern, item[1])

            table_dict[table_name] = table_columns

        return table_dict
    return None


def infomation_concat(pre_messages_input, pre_sql, value_all_info, error_info):
    pre_messages_object = pre_messages_input["messages"][0]
    pre_messages_info = pre_messages_object["content"]
    value_all_info = "###Value Examples:\n" + value_all_info + "\n\n"
    sql_info = "###Pre-SQL:\n" + pre_sql
    if error_info != "":
        error_info = "The column in the above sql has an error message:\n" + error_info
        second_messages_info = pre_messages_info + value_all_info + sql_info + "\n\n" + error_info
    else:
        second_messages_info = pre_messages_info + value_all_info + sql_info

    pre_messages_object["content"] = second_messages_info

    pre_messages_input["messages"] = pre_messages_input["messages"][:1]
    return pre_messages_input

def dataPrepare(pre_input_file_path, second_input_file_path, raw_format_file_path):
    pre_messages_list = []
    second_messages_list = []
    database_name_list = []
    with open(pre_input_file_path, 'r', encoding='utf-8') as file:
        for idx, line in enumerate(file):
            data = json.loads(line)
            messages = data['messages']
            pre_messages_list.append(data)

    with open(second_input_file_path, 'r', encoding='utf-8') as file:
        for idx, line in enumerate(file):
            data = json.loads(line)
            full_messages = data['messages']

            database_info = full_messages[0]
            database_name = database_info["database_name"]
            database_name_list.append(database_name)

            full_messages.pop(0)
            second_messages_list.append(data)

    with open(raw_format_file_path, 'r', encoding='utf-8') as file:
        raw_format_data = json.load(file)

    return pre_messages_list, second_messages_list, database_name_list, raw_format_data

def preSqlGenerate(message):
    try:
        response = client.chat.completions.create(
            messages=message['messages'],
            model=model_openai,
            temperature=0.7,
            top_p=0.9,
            presence_penalty=0,
            frequency_penalty=0
        )
        output_message = response.choices[0].message.content
        sql = extract_sql_query(output_message)
        format_SQL = {'messages': []}
        if sql is None:
            print("Pre_sql not extracted")
            format_SQL['messages'].append({"role": "assistant", "content": output_message})
            format_SQL['messages'].append({"role": "user", "content": SQL_FORMAT_PROMPT})
            response = client.chat.completions.create(
                messages=format_SQL['messages'],
                model=model_openai,
                temperature=0,
            )
            match = re.search(r'(?<=SQL:\s).+', response.choices[0].message.content)
            if match:
                sql = match.group()
            else:
                raise
        return sql
    except Exception as e:
        raise

def GSR(file_path_list, start_idx, end_idx):
    output_sql_list = []
    error_idx_list = []

    pre_messages_list, second_messages_list, database_name_list, raw_format_data = dataPrepare(file_path_list[0], file_path_list[1], file_path_list[2])

    second_sql = ""

    for idx, (pre_message, second_messages, database_name, current_format_item) in enumerate(
            tqdm(islice(zip(pre_messages_list, second_messages_list, database_name_list, raw_format_data), start_idx, end_idx),
                 total= (end_idx - start_idx))):
        try:
            pre_sql = preSqlGenerate(pre_message)
        except Exception as e:
            print(f"Error at index: {idx}" + str(e))
            error_idx_list.append(idx)
            pre_sql = "error"
            output_sql_list.append(pre_sql)
            continue

        db_file = file_path_list[3] + "/" + database_name + "/" + database_name + ".sqlite"
        text_input = text_extractor(second_messages["messages"][0]["content"])

        no_extract_pre_sql_flag = 0  # Unsuccessful extraction of pre_sql
        # Splice the value_info,error_info information into the prompt and let the model regenerate the sql, defining the new sql as the new pre_sql.
        openai_input = {}
        format_SQL_input = {'messages': []}
        n = 0
        while (n < 3):
            # Return Value information and error information
            pre_messages_input = copy.deepcopy(second_messages)
            value_all_info, error_info, current_table_dict = value_example_extractor(db_file, pre_sql, text_input)
            if error_info != "":
                n += 1
                openai_input = infomation_concat(pre_messages_input, pre_sql, value_all_info, error_info)
                response = client.chat.completions.create(
                    messages=openai_input['messages'],
                    model=model_openai,
                    temperature=0.2,
                )
                output_message = response.choices[0].message.content
                pre_sql = extract_sql_query(output_message)
                openai_input['messages'].append({"role": "assistant", "content": output_message})
                if pre_sql is None:
                    print("Pre_sql not extracted")
                    openai_input['messages'].append({"role": "user", "content": SQL_FORMAT_PROMPT})
                    response = client.chat.completions.create(
                        messages=openai_input['messages'],
                        model=model_openai,
                        temperature=0,
                    )
                    match = re.search(r'(?<=SQL:\s).+', response.choices[0].message.content)
                    if match:
                        pre_sql = match.group()
                    else:
                        error_idx_list.append(idx)
                        continue
                second_sql = pre_sql
            else:
                schema_regenerate_openai_input = transform_data_predict_symbol_column_description_hint(
                    file_path_list[3], current_format_item, current_table_dict)
                response = client.chat.completions.create(
                    messages=schema_regenerate_openai_input['messages'],
                    model=model_openai,
                    temperature=0.2,
                )
                output_message = response.choices[0].message.content  # Candidate schema ranges obtained by blocking out Pre-SQL partial Schema
                regenerate_extra_schema = extract_schema_info(output_message)
                if regenerate_extra_schema is None:
                    print("Schema not extracted")
                else:
                    # Iterate over dict2, removing list elements with the same key in dict1.
                    for key, value in current_table_dict.items():
                        if key in regenerate_extra_schema:
                            # Remove the values in dict2 from the list in dict1.
                            regenerate_extra_schema[key] = list(
                                set(regenerate_extra_schema[key]) - set(value))
                    value_all_info, error_extra_info = value_example_extractor_masked_extra_schema(db_file,
                                                                                                   regenerate_extra_schema,
                                                                                                   value_all_info,
                                                                                                   current_table_dict)

                openai_input = infomation_concat(pre_messages_input, pre_sql, value_all_info, error_info)
                response = client.chat.completions.create(
                    messages=openai_input['messages'],
                    model=model_openai,
                    temperature=0.2,
                )
                output_message = response.choices[0].message.content
                pre_sql = extract_sql_query(output_message)
                openai_input['messages'].append({"role": "assistant", "content": output_message})
                if pre_sql is None:
                    no_extract_pre_sql_flag = 1
                    print("Pre_sql not extracted")
                    openai_input['messages'].append({"role": "user", "content": SQL_FORMAT_PROMPT})
                    response = client.chat.completions.create(
                        messages=openai_input['messages'],
                        model=model_openai,
                        temperature=0,
                    )
                    match = re.search(r'(?<=SQL:\s).+', response.choices[0].message.content)
                    if match:
                        pre_sql = match.group()
                    else:
                        error_idx_list.append(idx)
                        n += 1
                        continue
                second_sql = pre_sql
                break

        result_second_sql, error_message_second_sql = one_sql_execute(db_file, second_sql)

        if error_message_second_sql != "":
            sql_execute_output_correct_prompt_back_part = ""
            if no_extract_pre_sql_flag:
                openai_input['messages'].pop()

            openai_content = openai_input['messages'][0]["content"]

            if "###hint" in openai_content.lower():
                sql_execute_output_correct_prompt_back_part = SQL_EXECUTE_OUTPUT_CORRECT_PROMPT_CHECK_OUTPUT_back_part_1
                pattern = r"(###Input:\n.*?\n\n###Hint:\n.*?\n\n)"
                match = re.search(pattern, openai_content, re.DOTALL)
                if match:
                    input_evidence = match.group(1)
                else:
                    error_idx_list.append(idx)
                    print(str(idx) + " Input and hint not found!!!")
            else:
                sql_execute_output_correct_prompt_back_part = SQL_EXECUTE_OUTPUT_CORRECT_PROMPT_CHECK_OUTPUT_back_part_2
                pattern = r"(###Input:\n(.*?)\n\n)"
                match = re.search(pattern, openai_content, re.DOTALL)
                if match:
                    input_evidence = match.group(1)
                else:
                    error_idx_list.append(idx)
                    print(str(idx) + " Input not found!!!")

            sql_correct_info = SQL_EXECUTE_OUTPUT_CORRECT_PROMPT + str(
                error_message_second_sql) + "\n\n" + input_evidence + sql_execute_output_correct_prompt_back_part
            openai_input['messages'].append({"role": "user", "content": sql_correct_info})
            response = client.chat.completions.create(
                messages=openai_input['messages'],
                model=model_openai,
                temperature=0.2,
            )
            output_message = response.choices[0].message.content
            final_sql = extract_sql_query(output_message)
            if final_sql is None:
                print(str(idx) + " No final_sql was extracted.")
                format_SQL_input['messages'].append({"role": "assistant", "content": output_message})
                format_SQL_input['messages'].append({"role": "user", "content": SQL_FORMAT_PROMPT})
                response = client.chat.completions.create(
                    messages=format_SQL_input['messages'],
                    model=model_openai,
                    temperature=0,
                )
                match = re.search(r'(?<=SQL:\s).+', response.choices[0].message.content)
                if match:
                    final_sql = match.group()
                else:
                    error_idx_list.append(idx)
                    final_sql = ""
        elif not result_second_sql or any(any(value is None for value in row) for row in result_second_sql):
            sql_execute_output_correct_prompt_back_part = ""
            if no_extract_pre_sql_flag:
                openai_input['messages'].pop()

            openai_content = openai_input['messages'][0]["content"]

            if "###hint" in openai_content.lower():
                sql_execute_output_correct_prompt_back_part = SQL_EXECUTE_OUTPUT_CORRECT_PROMPT_CHECK_OUTPUT_back_part_1
                pattern = r"(###Input:\n.*?\n\n###Hint:\n.*?\n\n)"
                match = re.search(pattern, openai_content, re.DOTALL)
                if match:
                    input_evidence = match.group(1)
                else:
                    error_idx_list.append(idx)
                    print(str(idx) + " Input and hint not found!!!")
            else:
                sql_execute_output_correct_prompt_back_part = SQL_EXECUTE_OUTPUT_CORRECT_PROMPT_CHECK_OUTPUT_back_part_2
                pattern = r"(###Input:\n(.*?)\n\n)"
                match = re.search(pattern, openai_content, re.DOTALL)
                if match:
                    input_evidence = match.group(1)
                else:
                    error_idx_list.append(idx)
                    print(str(idx) + " Input not found!!!")

            if len(result_second_sql) > 10:
                part_of_result_second_sql = result_second_sql[:5]
                sql_correct_info = SQL_EXECUTE_OUTPUT_CORRECT_PROMPT + str(
                    part_of_result_second_sql) + " (There are " + str(
                    len(result_second_sql)) + " records in total, only 5 are shown here.)" + "\n\n" + input_evidence + sql_execute_output_correct_prompt_back_part
            else:
                sql_correct_info = SQL_EXECUTE_OUTPUT_CORRECT_PROMPT + str(
                    result_second_sql) + "\n\n" + input_evidence + sql_execute_output_correct_prompt_back_part
            openai_input['messages'].append({"role": "user", "content": sql_correct_info})
            response = client.chat.completions.create(
                messages=openai_input['messages'],
                model=model_openai,
                temperature=0.2,
            )
            output_message = response.choices[0].message.content
            final_sql = extract_sql_query(output_message)
            if final_sql is None:
                print(str(idx) + " No final_sql was extracted.")
                format_SQL_input['messages'].append({"role": "assistant", "content": output_message})
                format_SQL_input['messages'].append({"role": "user", "content": SQL_FORMAT_PROMPT})
                response = client.chat.completions.create(
                    messages=format_SQL_input['messages'],
                    model=model_openai,
                    temperature=0,
                )
                match = re.search(r'(?<=SQL:\s).+', response.choices[0].message.content)
                if match:
                    final_sql = match.group()
                else:
                    error_idx_list.append(idx)
                    final_sql = ""
        else:
            sql_execute_output_correct_prompt_back_part = ""
            if no_extract_pre_sql_flag:
                openai_input['messages'].pop()

            openai_content = openai_input['messages'][0]["content"]
            if "###hint" in openai_content.lower():
                sql_execute_output_correct_prompt_back_part = SQL_EXECUTE_OUTPUT_CORRECT_PROMPT_CHECK_OUTPUT_back_part_1
                pattern = r"(###Input:\n.*?\n\n###Hint:\n.*?\n\n)"
                match = re.search(pattern, openai_content, re.DOTALL)
                if match:
                    input_evidence = match.group(1)
                else:
                    error_idx_list.append(idx)
                    print(str(idx) + " Input and hint not found!!!")
            else:
                sql_execute_output_correct_prompt_back_part = SQL_EXECUTE_OUTPUT_CORRECT_PROMPT_CHECK_OUTPUT_back_part_2
                pattern = r"(###Input:\n(.*?)\n\n)"
                match = re.search(pattern, openai_content, re.DOTALL)
                if match:
                    input_evidence = match.group(1)
                else:
                    error_idx_list.append(idx)
                    print(str(idx) + " Input not found!!!")

            if len(result_second_sql) > 10:
                part_of_result_second_sql = result_second_sql[:5]
                sql_correct_info = SQL_EXECUTE_OUTPUT_CORRECT_PROMPT + str(
                    part_of_result_second_sql) + " (There are " + str(
                    len(result_second_sql)) + " records in total, only 5 are shown here.)" + "\n\n" + input_evidence + sql_execute_output_correct_prompt_back_part
            else:
                sql_correct_info = SQL_EXECUTE_OUTPUT_CORRECT_PROMPT + str(
                    result_second_sql) + "\n\n" + input_evidence + sql_execute_output_correct_prompt_back_part
            openai_input['messages'].append({"role": "user", "content": sql_correct_info})
            response = client.chat.completions.create(
                messages=openai_input['messages'],
                model=model_openai,
                temperature=0.7,
                top_p=0.9,
                presence_penalty=0,
                frequency_penalty=0
            )
            output_message = response.choices[0].message.content
            final_sql = extract_sql_query(output_message)
            if final_sql is None:
                print(str(idx) + " No final_sql was extracted.")
                # 将sql在一行之中写出
                format_SQL_input['messages'].append({"role": "assistant", "content": output_message})
                format_SQL_input['messages'].append({"role": "user", "content": SQL_FORMAT_PROMPT})
                response = client.chat.completions.create(
                    messages=format_SQL_input['messages'],
                    model=model_openai,
                    temperature=0,
                )
                match = re.search(r'(?<=SQL:\s).+', response.choices[0].message.content)
                if match:
                    final_sql = match.group()
                else:
                    error_idx_list.append(idx)
                    final_sql = ""

        output_sql_list.append(final_sql)
        print(final_sql)


        with open(file_path_list[4], "w", encoding="utf-8") as file:
            for sql in output_sql_list:
                file.write(sql + "\n")

        with open(file_path_list[5], "w", encoding="utf-8") as file:
            for error_idx in list(set(error_idx_list)):
                file.write(str(error_idx) + "\n")

if __name__ == "__main__":

    # Reading files
    pre_input_file_path = '../data/openai_input/Pre_input.jsonl'
    second_input_file_path = '../data/openai_input/Second_input.jsonl'
    raw_format_file_path = '../data/raw_format_data/raw_format_data.json'
    database_file_path = '../data/database/dev_20240627/dev_databases'      # set
    output_file_path = '../output/GSR-dev.sql'
    error_file_path = '../output/error_idx/error_indices.txt'

    file_path_list = [pre_input_file_path, second_input_file_path, raw_format_file_path, database_file_path, output_file_path, error_file_path]

    # For a total of 1534 data, the values are assigned as follows. Start counting from 0 to 1533 for a total of 1534 data.
    start_idx = 0   # set
    end_idx = 1534  # set
    GSR(file_path_list, start_idx, end_idx)

    # If only the 0th data needs to be executed, the value is assigned as follows
    # start_idx = 0
    # end_idx = 1
    # GSR(file_path_list, start_idx, end_idx)
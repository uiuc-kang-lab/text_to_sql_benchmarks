import copy
import os
import json
import jsonlines
import sys
import re
import pandas as pd
from openai import OpenAI
from tqdm import tqdm
from data_process_config import API_KEYS, model_openai, DATA_PATH, INPUT_PROMPT, INSTRUCTION_PROMPT, SQL_DATA_INFO, DATABASE_PATH, PRESQL_HINT_PROMPT, PRESQL_PROMPT, SECOND_SQL_HINT_PROMPT, SECOND_SQL_PROMPT
from description_mapping import process_all_csv_files
ROOT_PATH = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.append(ROOT_PATH)

client = OpenAI(api_key=API_KEYS)

class ProcessSqlData:
    def __init__(self) -> None:
        pass

    def decode_json_file(
        self,
        data_file_list,
        table_file,
        db_folder_path,
        db_id_name,
        output_name
    ):
        """
        TO DO:
            1. Put the relevant prompt into the config.
            2. Put the field information of different data sources into the config.
        """

        if table_file.endswith(".jsonl"):
            tables = jsonlines.open(table_file)
            datas = []
            for data_file in data_file_list:
                datas.extend(jsonlines.open(data_file))

        elif table_file.endswith(".json"):
            tables = json.load(open(table_file))
            datas = []
            for data_file in data_file_list:
                datas.extend(json.load(open(data_file)))
        else:
            print("Unsupported file types")
            raise

        # First, take care of the table and columns for db_id
        db_dict = {}
        for item in tables:
            tables = item["table_names_original"]
            columns = item["column_names_original"][1:]
            primary_key = item["primary_keys"]
            foreign_keys = item["foreign_keys"]
            source = (
                item["db_id"] + " contains tables such as " + ", ".join(tables) + ". "
            )
            for i, name in enumerate(tables):
                data = [column[1] for column in columns if column[0] == i]

                source += (
                    "Table " + name + " has columns such as " + ", ".join(data) + ". "
                )

                # get primary key info
                for j in range(len(primary_key)):
                    if type(primary_key[j]) == int:
                        if columns[primary_key[j] - 1][0] == i:
                            source += (
                                columns[primary_key[j] - 1][1]
                                + " is the primary key."
                                + "\n"
                            )
                    # combination primary key
                    elif type(primary_key[j]) == list:
                        combine_p = "The combination of ("
                        keys = []
                        for k in range(len(primary_key[j])):
                            if columns[primary_key[j][k] - 1][0] == i:
                                keys.append(columns[primary_key[j][k] - 1][1])
                        if keys != []:
                            source += (
                                combine_p
                                + ", ".join(keys)
                                + ") are the primary key."
                                + "\n"
                            )
                    else:
                        print("not support type", type(primary_key[j]))
                        continue

            # get foreign key info
            for key in foreign_keys:
                source += (
                    "The "
                    + columns[key[0] - 1][1]
                    + " of "
                    + tables[columns[key[0] - 1][0]]
                    + " is the foreign key of "
                    + columns[key[1] - 1][1]
                    + " of "
                    + tables[columns[key[1] - 1][0]]
                    + ".\n"
                )

            db_dict[item["db_id"]] = source

        res = []
        base_instruction = INSTRUCTION_PROMPT

        for data in tqdm(datas):
            if data[db_id_name] in db_dict.keys():
                input = {
                    "db_id": data[db_id_name],
                    "instruction": base_instruction.format(
                        db_dict[data[db_id_name]]
                    ),
                    "input": INPUT_PROMPT.format(data["question"]),
                    "output": data[output_name],
                    "evidence": data["evidence"],
                    "history": [],
                }
                res.append(input)
        return res

    def create_sft_raw_data(self):
        database_path = os.path.join(DATA_PATH, "database")
        data = []
        for data_info in SQL_DATA_INFO:
            data_file_list = [
                os.path.join(database_path, data_info["data_source"], file)
                for file in data_info["file"]
            ]
            data.extend(
                self.decode_json_file(
                    data_file_list=data_file_list,
                    table_file=os.path.join(
                        database_path,
                        data_info["data_source"],
                        data_info["tables_file"],
                    ),
                    db_folder_path=os.path.join(
                        database_path,
                        data_info["data_source"],
                        data_info["database_name"],
                    ),
                    db_id_name=data_info["db_id_name"],
                    output_name=data_info["output_name"]
                )
            )

        return data

def insert_hint(input_string, hint_string):
    # Index to finding the meaning of ###Sentence Explanation:
    sentence_idx = input_string.find("###Sentence meaning explained:")

    if sentence_idx != -1:
        result = input_string[:sentence_idx] + hint_string + input_string[sentence_idx:]
    else:
        result = input_string + hint_string

    return result

def convert_to_structured_format_column_description(input_string, database_root):
    # Format the complete schema information, including structure, column_description, value_description
    lines = input_string.strip().split('\n')
    structured_string = lines[0] + "\n"

    database_name = structured_string.split(" ")[0]
    db_file = database_root + "/" + database_name + "/" + database_name + ".sqlite"
    tables = {}
    foreign_keys = []

    for line in lines[1:]:
        if line.startswith("Table"):
            parts = line.split(" has columns such as ")
            table_name = parts[0].split()[1]
            columns_info = parts[1]
            primary_key = None
            if "primary key" in columns_info:
                columns_part, primary_key_part = columns_info.rsplit(". ", 1)
                if "is the primary key" in primary_key_part:
                    primary_key = primary_key_part.split(" is the primary key")[0].strip().replace(".", "")
                elif "are the primary key" in primary_key_part:
                    primary_key = primary_key_part
                else:
                    print("No primary key found.")
            else:
                columns_part = columns_info
            columns = columns_part.replace(".", "").split(", ")
            tables[table_name] = {
                "columns": columns,
                "primary_key": primary_key,
                "foreign_keys": []
            }
        elif "foreign key" in line:
            foreign_keys.append(line)

    for fk in foreign_keys:
        fk_parts = fk.split(" is the foreign key of ")
        col_table = fk_parts[0].split("The ")[1]
        col, table = col_table.split(" of ")
        ref_col, ref_table = fk_parts[1].split(" of ")
        tables[table]["foreign_keys"].append(f"{col} -> {ref_table}({ref_col})")

    for table, details in tables.items():
        table_database = db_file.rsplit('/', 2)[1] + "/" + table.lower() + ".csv"
        structured_string += f"-Table: {table}:\n"
        for column in details['columns']:
            column_description = all_mappings[table_database]['column_description_mapping'].get(column)
            structured_string += f"\t-Column: {column}\n"
            if column_description is not None and not pd.isna(column_description):
                structured_string += f"\t\t-Column_description: {column_description}\n"
        if details["primary_key"]:
            structured_string += f"\t-Primary Key: {details['primary_key']}\n"
        if details["foreign_keys"]:
            structured_string += f"\t-Foreign Keys: {', '.join(details['foreign_keys'])}\n"

    return structured_string.strip()

def convert_to_structured_format_no_description(input_string):
    # Formatting the schema structure
    lines = input_string.strip().split('\n')
    structured_string = lines[0] + "\n"

    tables = {}
    foreign_keys = []

    for line in lines[1:]:
        if line.startswith("Table"):
            parts = line.split(" has columns such as ")
            table_name = parts[0].split()[1]
            columns_info = parts[1]
            primary_key = None
            if "primary key" in columns_info:
                columns_part, primary_key_part = columns_info.rsplit(". ", 1)
                if "is the primary key" in primary_key_part:
                    primary_key = primary_key_part.split(" is the primary key")[0].strip().replace(".", "")
                elif "are the primary key" in primary_key_part:
                    primary_key = primary_key_part
                else:
                    print("No primary key found.")
            else:
                columns_part = columns_info
            columns = columns_part.replace(".", "").split(", ")
            tables[table_name] = {
                "columns": columns,
                "primary_key": primary_key,
                "foreign_keys": []
            }
        elif "foreign key" in line:
            foreign_keys.append(line)

    for fk in foreign_keys:
        fk_parts = fk.split(" is the foreign key of ")
        col_table = fk_parts[0].split("The ")[1]
        col, table = col_table.split(" of ")
        ref_col, ref_table = fk_parts[1].split(" of ")
        tables[table]["foreign_keys"].append(f"{col} -> {ref_table}({ref_col})")

    for table, details in tables.items():
        structured_string += f"Table {table}:\n"
        structured_string += f"  Columns: {', '.join(details['columns'])}\n"
        if details["primary_key"]:
            structured_string += f"  Primary Key: {details['primary_key']}\n"
        if details["foreign_keys"]:
            structured_string += f"  Foreign Keys: {', '.join(details['foreign_keys'])}\n"

    return structured_string.strip()

def split_string(input_string):
    parts = input_string.split("\n##Instruction:\n")
    if len(parts) == 2:
        return parts[0], parts[1]
    else:
        return input_string, None

def transform_data_pre(data, database_root):
    transformed_data = []
    error_mes = []
    for idx, item in enumerate(data[:]):
        try:
            instruction = item["instruction"]
            part1, part2 = split_string(instruction)
            structured_string = convert_to_structured_format_column_description(part2, database_root)

            pattern = r"^(.*?)\s+contains"
            database_name = re.search(pattern, structured_string).group(1).strip()

            input_change = item["input"].replace("\n\n###Response:", '')
            if item["evidence"] != "":
                instruction = PRESQL_HINT_PROMPT
                evidence = "###Hint:\n" + item["evidence"] + "\n\n"
                input_change = insert_hint(input_change, evidence)
            else:
                instruction = PRESQL_PROMPT

            input = "###Database schema:\n" + structured_string + "\n\n" + input_change.replace(
                "###Sentence meaning explained", "###Logic Clause")

            final_input = instruction + "\n\n" + input
            transformed_item = {
                "messages": [
                    {"role": "user", "content": final_input}
                ]
            }
            transformed_data.append(transformed_item)
        except Exception as e:
            error = str(idx) + str(e)
            error_mes.append(error)
    error_file = os.path.join(DATA_PATH, "openai_input/error_pre.txt")
    with open(error_file, 'w', encoding='utf-8') as f:
        for item in error_mes:
            f.write(item)
    return transformed_data

def transform_data_second(data):
    transformed_data = []
    error_mes =[]
    for idx, item in enumerate(data[:]):
        try:
            instruction = item["instruction"]
            part1, part2 = split_string(instruction)
            structured_string = convert_to_structured_format_no_description(part2)

            pattern = r"^(.*?)\s+contains"
            database_name = re.search(pattern, structured_string).group(1).strip()

            match = re.search(r'###Input:\n(.*?)(?=\n###|$)', item["input"], re.DOTALL)
            input_change = item["input"].replace("###Response:", '')
            if item["evidence"] != "":
                instruction = SECOND_SQL_HINT_PROMPT
                evidence = "###Hint:\n" + item["evidence"] + "\n\n"
                input_change = insert_hint(input_change, evidence)
            else:
                instruction = SECOND_SQL_PROMPT

            input = "###Database schema:\n" + structured_string + "\n\n" + input_change

            final_input = instruction + "\n\n" + input
            transformed_item = {
                "messages": [
                    {"database_name": database_name},
                    {"role": "user", "content": final_input}
                ]
            }
            transformed_data.append(transformed_item)
        except Exception as e:
            error = str(idx) + str(e)
            error_mes.append(error)
    error_file = os.path.join(DATA_PATH, "openai_input/error_second.txt")
    with open(error_file, 'w', encoding='utf-8') as f:
        for item in error_mes:
            f.write(item)
    return transformed_data

def update_instructions(data):
    for item in data:
        instruction = item["instruction"]
        part1, part2 = split_string(instruction)
        part1_end = part2.split(' ', 1)[1].split('.')[0] + '. '
        part1_end_fix = part1_end.strip()

        if part1_end in instruction:
            updated_instruction = instruction.replace(part1_end, part1_end_fix + '\n', 1)
            updated_instruction = re.sub(r'\.\s*Table', '.\nTable', updated_instruction)
            item['instruction'] = updated_instruction
    return data

def write_to_file(transformed_data, filename):
    with open(filename, 'w', encoding='utf-8') as f:
        for index, item in enumerate(transformed_data):
            f.write(json.dumps(item, ensure_ascii=False) + "\n")

def write_raw_format_data(transformed_data, filename):
    with open(filename, 'w', encoding='utf-8') as f:
        f.write(json.dumps(transformed_data, indent=4))

def extract_sentence(input_string):
    match = re.search(r'###Input:\n(.*?)\n\n###Response:', input_string, re.DOTALL)
    if match:
        return match.group(1)
    else:
        print("none")
        return None

def insert_explanation(input_string, sentence_meaning):
    insertion = "###Sentence meaning explained:\n" + sentence_meaning + "\n\n"
    return input_string.replace("###Response:", insertion + "###Response:")

def easysentence_process(process_data):
    output_data = process_data

    questions = []
    for item in process_data:
        question = item["input"]
        questions.append(question)

    # 存储错误的列表
    error_indices = []

    for index, item in enumerate(tqdm(process_data[:], desc="Processing")):
        question = item["input"]
        extracted_question = extract_sentence(question)
        message = "**Sentence**" + ": \'" + extracted_question + "\'" + "\n\nBreak the above sentence into simpler sentences based on their logical structure, and list them point by point in numerical order. Return only the simplified sentences in the specified numerical order."
        # "\n\nBreak the above sentence down into simple sentences and list them point by point in numerical order, returning only the simple sentences listed in numerical order."
        try:
            response = client.chat.completions.create(
                messages=[
                    {
                        "role": "user",
                        "content": message,
                    }
                ],
                model=model_openai,
                temperature=0.2,
                max_tokens=4096
            )
            output_message = response.choices[0].message.content
            #print(output_message)

            output_data[index]["input"] = insert_explanation(output_data[index]["input"], output_message)
        except Exception as e:
            print(f"Error at index: {index}")
            print(e)
            error_indices.append(index)

    with open(r"./error_info/error_index", 'w', encoding='utf-8') as error_file:
        for error_index in error_indices:
            error_file.write(json.dumps({"index": error_index}) + '\n')

    return output_data

if __name__ == "__main__":
    # Specify the root folder path, call the function to process all CSV files
    database_root_folder = os.path.join(DATA_PATH, DATABASE_PATH).replace("\\","/")
    all_mappings = process_all_csv_files(database_root_folder)
    save_mappings_file = os.path.join(DATA_PATH, "mapping/all_mappings.json")
    # Save the dictionary as a json file
    with open(save_mappings_file, 'w') as f:
        json.dump(all_mappings, f)

    precess = ProcessSqlData()
    data = precess.create_sft_raw_data()
    update_data = update_instructions(data)
    raw_format_data = os.path.join(DATA_PATH,"raw_format_data/raw_format_data.json")

    easy_sentence_data = copy.deepcopy(update_data)
    easy_sentence_data = easysentence_process(easy_sentence_data)
    write_raw_format_data(easy_sentence_data, raw_format_data)

    transformed_data_pre = transform_data_pre(easy_sentence_data, database_root_folder)
    openai_input_data_pre = os.path.join(DATA_PATH, "openai_input/Pre_input.jsonl")
    write_to_file(transformed_data_pre, openai_input_data_pre)

    transformed_data_second = transform_data_second(update_data)
    openai_input_data_second = os.path.join(DATA_PATH, "openai_input/Second_input.jsonl")
    write_to_file(transformed_data_second, openai_input_data_second)

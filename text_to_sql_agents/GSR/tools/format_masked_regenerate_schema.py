import json
import re

import pandas as pd

from .tools_config import HINT_SQL_REGENERATE_SYMBOL_FORMAT_PROMPT, NO_HINT_SQL_REGENERATE_SYMBOL_FORMAT_PROMPT


with open(r'../data/mapping/all_mappings.json', 'r') as f:
    all_mappings = json.load(f)

def insert_hint(input_string, hint_string):
    sentence_idx = input_string.find("###Sentence meaning explained:")

    if sentence_idx != -1:
        result = input_string[:sentence_idx] + hint_string + input_string[sentence_idx:]
    else:
        result = input_string + hint_string

    return result

def split_string(input_string):
    parts = input_string.split("\n##Instruction:\n")
    if len(parts) == 2:
        return parts[0], parts[1]
    else:
        return input_string, None


def convert_to_structured_format_column_description(database_file_path, input_string, current_table_dict):
    # Format the complete schema information, including structure, column_description, value_description
    lines = input_string.strip().split('\n')
    structured_string = lines[0] + "\n"

    database_name = structured_string.split(" ")[0]
    db_file = database_file_path + "/" + database_name + "/" + database_name + ".sqlite"
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
            if current_table_dict.get(table) is None or column not in current_table_dict[table]:
                column_description = all_mappings[table_database]['column_description_mapping'].get(column)
                structured_string += f"\t-Column: {column}\n"
                if column_description is not None and not pd.isna(column_description):
                    structured_string += f"\t\t-Column_description: {column_description}\n"
        if details["primary_key"]:
            structured_string += f"\t-Primary Key: {details['primary_key']}\n"
        if details["foreign_keys"]:
            structured_string += f"\t-Foreign Keys: {', '.join(details['foreign_keys'])}\n"

    return structured_string.strip()

def transform_data_predict_symbol_column_description_hint(database_file_path, item, current_table_dict):
    try:
        instruction = item["instruction"]
        part1, part2 = split_string(instruction)
        structured_string = convert_to_structured_format_column_description(database_file_path, part2, current_table_dict)

        pattern = r"^(.*?)\s+contains"
        database_name = re.search(pattern, structured_string).group(1).strip()

        input_change = item["input"].replace("\n\n###Response:", '')
        if item["evidence"] != "":
            instruction = HINT_SQL_REGENERATE_SYMBOL_FORMAT_PROMPT
            hint = "###Hint:\n" + item["evidence"] + "\n\n"
            input_change = insert_hint(input_change, hint)
        else:
            instruction = NO_HINT_SQL_REGENERATE_SYMBOL_FORMAT_PROMPT

        input = "###Database schema:\n" + structured_string + "\n\n" + input_change.replace("###Sentence meaning explained","###Logic Clause")

        final_input = instruction + "\n\n" + input
        transformed_item = {
            "messages": [
                {"role": "user", "content": final_input}
            ]
        }
    except Exception as e:
        print(e)
    return transformed_item
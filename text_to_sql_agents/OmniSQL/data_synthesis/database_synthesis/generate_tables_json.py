import json
import sqlite3
import os
import re
from tqdm import tqdm

def obtain_db_ddls(db_file_dir):
    conn = sqlite3.connect(db_file_dir)
    cursor = conn.cursor()

    cursor.execute("SELECT name, sql FROM sqlite_master WHERE type='table';")
    tables = cursor.fetchall()

    create_statements = []
    for table in tables:
        _, create_statement = table
        create_statements.append(create_statement)

    cursor.close()
    conn.close()

    return create_statements

def obtain_pks(db_file_dir, table_name):
    conn = sqlite3.connect(db_file_dir)
    cursor = conn.cursor()

    cursor.execute("SELECT name, type, pk FROM PRAGMA_TABLE_INFO('{}')".format(table_name))
    results = cursor.fetchall()
    # print(results)

    column_names = [result[0] for result in results]
    column_types = [result[1] for result in results]
    pk_indicators = [result[2] for result in results]
    pk_columns = [column_name for column_name, pk_indicator in zip(column_names, pk_indicators) if pk_indicator == 1]
    
    return [f'"{table_name}"."{pk_column}"' for pk_column in pk_columns]

def obtain_fks(db_file_dir, table_name):
    conn = sqlite3.connect(db_file_dir)
    cursor = conn.cursor()

    # obtain foreign keys in the current table
    cursor.execute("SELECT * FROM pragma_foreign_key_list('{}');".format(table_name))
    results = cursor.fetchall()

    foreign_keys = []
    for result in results:
        if None not in [result[3], result[2], result[4]]:
            foreign_keys.append([f'"{table_name}"."{result[3]}"', f'"{result[2]}"."{result[4]}"'])

    return foreign_keys

if __name__ == "__main__":
    db_ids = os.listdir("./synthetic_sqlite_databases")

    tables = []
    for db_id in tqdm(db_ids):
        table = dict()
        table["db_id"] = db_id
        table["ddls"] = []
        table["column_names"] = [[-1, "*"]]
        table["column_names_original"] = [[-1, "*"]]
        table["column_types"] = ["text"]
        table["table_names"] = []
        table["table_names_original"] = []
        table["foreign_keys"] = []
        table["primary_keys"] = []

        db_file_dir = os.path.join("synthetic_sqlite_databases", db_id, db_id + ".sqlite")
        ddls = obtain_db_ddls(db_file_dir)
        # print("\n\n".join(ddls))

        primary_keys_info = []
        foreign_keys_info = []

        table_column_names = ["*"]
        for table_idx, ddl in enumerate(ddls):
            if ddl.count("PRIMARY KEY") > 1:
                print(ddl)
            table["ddls"].append(ddl)
            table_name_match = re.search(r'CREATE TABLE\s+"([^"]+)"', ddl)
            table_name = table_name_match.group(1) if table_name_match else None
            if table_name is None:
                continue

            table["table_names"].append(table_name)
            table["table_names_original"].append(table_name)
            column_infos = re.findall(r'"([^"]+)"\s+(\w+)\s*/\*\s*(.*?)\s*\*/', ddl)

            # print(f"Table Name: {table_name}")
            for column_name, column_type, comment in column_infos:
                # print(f"Column Name: {column_name}, Type: {column_type}, Comment: {comment}")
                table["column_names"].append([table_idx, comment]) # column_names is the semantic names (i.e., descriptions) of columns
                table["column_names_original"].append([table_idx, column_name]) # column_names_original is the original names used in DDLs
                table["column_types"].append(column_type)
                table_column_names.append(f'"{table_name}"."{column_name}"')

            primary_keys_info.append(obtain_pks(db_file_dir, table_name))
            foreign_keys_info.extend(obtain_fks(db_file_dir, table_name))

        for primary_key_info in primary_keys_info:
            try:
                if len(primary_key_info) == 1:
                    table["primary_keys"].append(table_column_names.index(primary_key_info[0]))
                elif len(primary_key_info) > 1:
                    pk_idx_list = []
                    for primary_key_info_str in primary_key_info:
                        pk_idx_list.append(table_column_names.index(primary_key_info_str))
                    table["primary_keys"].append(pk_idx_list)
            except Exception as e:
                print(primary_key_info)
                # print(db_id)
                print(e)

        for foreign_key_info in foreign_keys_info:
            try:
                table["foreign_keys"].append(
                    [table_column_names.index(foreign_key_info[0]), table_column_names.index(foreign_key_info[1])]
                )
            except Exception as e:
                print(foreign_key_info)
                # print(db_id)
                print(e)
        
        tables.append(table)

    with open("tables.json", "w", encoding="utf-8") as f:
        f.write(json.dumps(tables, ensure_ascii=False, indent=2))
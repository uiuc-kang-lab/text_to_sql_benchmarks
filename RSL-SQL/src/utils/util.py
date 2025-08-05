import pandas as pd
import sqlite3
import threading
import os
import sqlglot
from configs.config import dev_databases_path



def execute_sql_threaded(sql, db_name, result_container):
    db_path = f'{dev_databases_path}/{db_name}/{db_name}.sqlite'
    conn = None
    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()

        cursor.execute(sql)
        results = cursor.fetchall()
        result_container['row_count'] = len(results)
        result_container['column_count'] = len(results[0]) if results else 0
        result_container['result_preview'] = str(results[:5])

    except Exception as e:
        result_container['error'] = str(e)

    finally:
        if conn:
            conn.close()


def execute_sql(sql, db_name, timeout=30):
    result_container = {}
    thread = threading.Thread(target=execute_sql_threaded, args=(sql, db_name, result_container))
    thread.start()
    thread.join(timeout)

    if thread.is_alive():
        # 超时处理
        return 0, 0, "TimeoutError: The SQL query took too long to execute. Please optimize your SQL query."
    else:
        # 返回结果
        if 'error' in result_container:
            return 0, 0, result_container['error']
        return result_container.get('row_count', 0), result_container.get('column_count', 0), result_container.get(
            'result_preview', "")


# execute_sql('SELECT `code` FROM `drivers` ORDER BY `dob` DESC LIMIT 3; SELECT COUNT(*) FROM (SELECT `nationality` FROM `drivers` ORDER BY `dob` DESC LIMIT 3) AS T WHERE T.`nationality` = \'Dutch\'','formula_1')

# 根据sql语句获取最后一个单词和去掉最后一个单词的sql语句
# sql语句的最后一个单词为数据库名
# def get_last_word_and_trimmed_sql(sql_query):
#     # Split the string into words
#     words = sql_query.split()
#     # Get the last word
#     last_word = words[-1]
#     # Get the SQL query without the last word
#     trimmed_sql = " ".join(words[:-1])
#     return last_word, trimmed_sql
#
#
# # 从文件中查找字符串
#
# def find_string_in_file(filename, target_string):
#     line_numbers = []
#     with open(filename, 'r') as file:
#         for line_number, line in enumerate(file, start=1):
#             if target_string in line:
#                 line_numbers.append(line_number)
#     return line_numbers
#
#
#
#
#
# # 将json文件分为四份
# def split_json(json_file,name):
#     # 读取json文件
#     with open(json_file, 'r') as f:
#         data = json.load(f)
#
#     # 计算每份的大小
#     size = len(data) // 4
#
#     # 将数据分为四份
#     data1 = data[:size]
#     data2 = data[size:2*size]
#     data3 = data[2*size:3*size]
#     data4 = data[3*size:]
#
#     # 将四份数据分别写入新的json文件
#     with open(f'{name}_file1.json', 'w') as f:
#         json.dump(data1, f, indent=4)
#     with open(f'{name}_file2.json', 'w') as f:
#         json.dump(data2, f, indent=4)
#     with open(f'{name}_file3.json', 'w') as f:
#         json.dump(data3, f, indent=4)
#     with open(f'{name}_file4.json', 'w') as f:
#         json.dump(data4, f, indent=4)
#
#
# # 将txt文件分为四份
# def split_txt(txt_file, output_prefix):
#     # 读取txt文件
#     with open(txt_file, 'r') as f:
#         lines = f.readlines()
#
#     # 计算每份的大小
#     size = len(lines) // 4
#
#     # 将数据分为四份
#     lines1 = lines[:size]
#     lines2 = lines[size:2*size]
#     lines3 = lines[2*size:3*size]
#     lines4 = lines[3*size:]
#
#     # 将四份数据分别写入新的txt文件
#     with open(f'{output_prefix}_file1.txt', 'w') as f:
#         f.writelines(lines1)
#     with open(f'{output_prefix}_file2.txt', 'w') as f:
#         f.writelines(lines2)
#     with open(f'{output_prefix}_file3.txt', 'w') as f:
#         f.writelines(lines3)
#     with open(f'{output_prefix}_file4.txt', 'w') as f:
#         f.writelines(lines4)
#
#
# # 将四份数据合并为一份
# def merge_json(output_file):
#     with open('output_file1.json', 'r') as f:
#         datas1 = json.load(f)
#
#     with open('output_file2.json', 'r') as f:
#         datas2 = json.load(f)
#
#     with open('output_file3.json', 'r') as f:
#         datas3 = json.load(f)
#
#     with open('output_file4.json', 'r') as f:
#         datas4 = json.load(f)
#
#     datas = datas1 + datas2 + datas3 + datas4
#
#     with open(output_file, 'w') as f:
#         json.dump(datas, f, indent=4)
#
#
# def merge_sqltxt(output_files, output_file):
#     line_list = []
#     for i in range(len(output_files)):
#         with open('split_output/'+output_files[i], 'r') as f:
#             lines = f.readlines()
#         line_list += lines
#
#     lines = [line.strip() for line in line_list]
#
#     my_list = [item + '\n' for item in lines]
#
#     with open(output_file, 'w') as f:
#         f.writelines(my_list)
#
# def merge_json(output_files, output_file):
#     data_list = []
#     for i in range(len(output_files)):
#         with open('split_information/'+output_files[i], 'r') as f:
#             data = json.load(f)
#         data_list += data
#
#     with open(output_file, 'w') as f:
#         json.dump(data_list, f, indent=4, ensure_ascii=False)

def simple_throw_row_data(db_name,tables,table_list):

    # 动态加载前三行数据
    simplified_ddl_data = []
    # 读取数据库
    mydb = sqlite3.connect(
        fr"{dev_databases_path}/{db_name}/{db_name}.sqlite")  # 链接数据库
    cur = mydb.cursor()
    # 表

    Tables = tables  # Tables 为元组列表
    for table in Tables:
        # 列
        col_name_list = table_list[table]
        column_str = ",".join(col_name_list)
        cur.execute(f"select {column_str} from `{table}`")
        # col_name_list = [tuple[0] for tuple in cur.description]
        # print(col_name_list)
        db_data_all = []
        # 获取前三行数据
        for i in range(3):
            db_data_all.append(cur.fetchone())
        # ddls_data
        test = ""
        for idx, column_data in enumerate(col_name_list):
            # print(list(db_data_all[2])[idx])
            try:
                test += f"{column_data}[{list(db_data_all[0])[idx]},{list(db_data_all[1])[idx]},{list(db_data_all[2])[idx]}],"
            except:
                test = test
        simplified_ddl_data.append(f"{table}({test[:-1]})")
    ddls_data = "# " + ";\n# ".join(simplified_ddl_data) + ";\n"

    return ddls_data


def get_describe(db,tables,table_list):

    describe = "#\n# "
    for table in tables:
        with open(f'/Users/mac/Desktop/bird/dev_20240627/dev_databases/{db}/database_description/{table}.csv', 'r') as file:
            data = pd.read_csv(file)
        describe+= table + "("
        for column in table_list[table]:

            for index, row in data.iterrows():
                original_column_name= row['original_column_name']
                if column.replace('`','').lower().strip() == row['original_column_name'].lower().strip():
                    data_format = row['data_format']
                    if str(row['column_description']).strip() == 'nan':
                        describe+= f"`this data_format of the column is '{data_format}',the description of the column is '{column.replace('`','')}'`,"
                    else:
                        # print(str(row['column_description']))
                        describe+= f"`this data_format of the column is '{data_format}',the description of the column is '{str(row['column_description'])}'`,"
        describe = describe[:-1]+")\n# "
    return describe.strip()


# 从一个sqlite数据库文件中，提取出所有的表名和列名
def get_tables_and_columns(sqlite_db_path):
    with sqlite3.connect(sqlite_db_path) as conn:
        cursor = conn.cursor()
        tables = cursor.execute("SELECT name FROM sqlite_master WHERE type='table';").fetchall()
        return [
            f"{_table[0]}.{_column[1]}"
            for _table in tables
            for _column in cursor.execute(f"PRAGMA table_info('{_table[0]}');").fetchall()
        ]


# 利用sqlglot工具，从一个sql语句中，提取出其中涉及的所有表和列（但是无法确认表与列之间的严格对应关系）
def extract_tables_and_columns(sql_query):
    parsed_query = sqlglot.parse_one(sql_query, read="sqlite")
    table_names = parsed_query.find_all(sqlglot.exp.Table)
    column_names = parsed_query.find_all(sqlglot.exp.Column)
    return {
        'table': {_table.name for _table in table_names},
        'column': {_column.alias_or_name for _column in column_names}
    }


def get_all_schema():
    # 读取所有数据库
    db_base_path = dev_databases_path
    db_schema = {}
    for db_name in os.listdir(db_base_path):
        db_path = os.path.join(db_base_path, db_name, db_name + '.sqlite')
        if os.path.exists(db_path):
            db_schema[db_name] = get_tables_and_columns(db_path)
    return db_schema






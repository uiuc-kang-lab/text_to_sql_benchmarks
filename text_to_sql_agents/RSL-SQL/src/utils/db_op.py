import sqlite3
from configs.config import dev_databases_path

def connect_to_db(db_name):
    return sqlite3.connect(dev_databases_path+'/' + db_name + f'/{db_name}.sqlite')

def get_all_table_names(db_name):
    conn = connect_to_db(db_name)
    cursor = conn.cursor()

    cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name != 'sqlite_sequence';")
    table_names = cursor.fetchall()

    conn.close()

    return [name[0] for name in table_names]

def get_all_column_names(db_name, table_name):
    conn = connect_to_db(db_name)
    cursor = conn.cursor()

    cursor.execute(f"PRAGMA table_info('{table_name}');")
    table_info = cursor.fetchall()

    column_names = [column[1] for column in table_info]

    conn.close()

    return column_names

def get_foreign_key_info(db_name, table_name):
    conn = connect_to_db(db_name)
    cursor = conn.cursor()

    cursor.execute(f"PRAGMA foreign_key_list('{table_name}');")
    foreign_key_info = cursor.fetchall()

    conn.close()

    return foreign_key_info

def get_table_infos(database_name):
    table_list = get_all_table_names(database_name)
    table_str = '#\n# '
    for table in table_list:
        column_list = get_all_column_names(database_name, table)

        column_list = ['`' + column + '`' for column in column_list]

        columns_str = f'{table}(' + ', '.join(column_list) + ')'

        table_str += columns_str + '\n# '

    return table_str

## 外键信息
def get_foreign_key_infos(database_name):
    table_list = get_all_table_names(database_name)

    foreign_str = '#\n# '
    for table in table_list:
        foreign_lists = get_foreign_key_info(database_name, table)

        for foreign in foreign_lists:
            foreign_one = f'{table}({foreign[3]}) references {foreign[2]}({foreign[4]})'
            foreign_str += foreign_one + '\n# '
            # print(foreign_one)

    return foreign_str

def get_throw_row_data(db_name):
    # 动态加载前三行数据
    simplified_ddl_data = []
    # 读取数据库
    mydb = connect_to_db(db_name)  # 链接数据库
    cur = mydb.cursor()
    # 表
    cur.execute("SELECT name FROM sqlite_master WHERE type='table'")
    Tables = cur.fetchall()  # Tables 为元组列表
    for table in Tables:
        # 列
        cur.execute(f"select * from `{table[0]}`")
        col_name_list = [tuple[0] for tuple in cur.description]
        # print(col_name_list)
        db_data_all = []
        # 获取前三行数据
        for i in range(3):
            db_data_all.append(cur.fetchone())
        # ddls_data
        test = ""
        for idx, column_data in enumerate(col_name_list):
            try:
                test += f"`{column_data}`[{list(db_data_all[0])[idx]},{list(db_data_all[1])[idx]},{list(db_data_all[2])[idx]}],"
            except:
                test = test
        simplified_ddl_data.append(f"{table[0]}({test[:-1]})")
    ddls_data = "# " + ";\n# ".join(simplified_ddl_data) + ";\n"

    return ddls_data

from utils.util import simple_throw_row_data
import json

def simplified(ppl):
    db = ppl['db']
    foreign_key = ppl['foreign_key'].strip()
    tables = ppl['tables']
    columns = ppl['columns']


    # 简化ddl
    table_list = {}
    simple_ddl_simple = "#\n# "
    for table in tables:
        simple_ddl_simple += table + "("
        column_list = []
        for column in columns:
            _table = column.split(".")[0].strip()
            if _table == table:
                column = column.split(".")[1].strip()
                column_list.append(column)
                simple_ddl_simple += column + ","
        table_list[table] = column_list
        simple_ddl_simple = simple_ddl_simple[:-1] + ")\n# "
    simple_ddl = simple_ddl_simple.strip()

    # 简化data
    data_ddl = simple_throw_row_data(db, tables, table_list)
    ddl_data = "#\n" + data_ddl.strip() + "\n# "

    # 简化foreign_key
    temp = "#\n"
    for line in foreign_key.split("\n"):
        try:
            table1 = line.split("# ")[1].split("(")[0].strip()
            table2 = line.split("references ")[1].split("(")[0].strip()
            if table1.lower() in tables and table2.lower() in tables:
                temp += line + "\n"
        except:
            continue
    foreign_key = temp.strip() + "\n# "
    return simple_ddl, ddl_data, foreign_key

def explanation_collection(ppl):

    with open('data/column_meaning.json', 'r') as f:
        column_meaning = json.load(f)

    tables = ppl['tables']
    columns = ppl['columns']
    db = ppl['db']

    columns = [obj.replace('`', '').lower() for obj in columns]
    columns = [obj.replace('.', '.`') + '`' for obj in columns]

    ### 收集解释
    explanation = ""

    for x in column_meaning:
        h = x
        x = x.lower().split("|")
        db_name = x[0]
        table_name = x[1]
        column_name = x[2]
        if db == db_name:
            if table_name in tables:
                if table_name + '.`' + column_name + '`' in columns:
                    explanation += f"### {table_name}.{column_name}: {column_meaning[h]}\n"

    explanation = explanation.replace("### ", "# ")

    return explanation
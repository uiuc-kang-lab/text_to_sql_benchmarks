import pandas as pd
import re, sqlite3, os, chardet


def find_foreign_keys_MYSQL_like(DATASET_JSON, db_name):
    schema_df = pd.read_json(DATASET_JSON)
    schema_df = schema_df.drop(['column_names', 'table_names'], axis=1)
    f_keys = []
    for index, row in schema_df.iterrows():
        tables = row['table_names_original']
        col_names = row['column_names_original']
        foreign_keys = row['foreign_keys']
        for foreign_key in foreign_keys:
            first, second = foreign_key
            first_index, first_column = col_names[first]
            second_index, second_column = col_names[second]
            f_keys.append([
                row['db_id'], tables[first_index], tables[second_index],
                first_column, second_column
            ])
    spider_foreign = pd.DataFrame(f_keys,
                                  columns=[
                                      'Database name', 'First Table Name',
                                      'Second Table Name',
                                      'First Table Foreign Key',
                                      'Second Table Foreign Key'
                                  ])

    df = spider_foreign[spider_foreign['Database name'] == db_name]
    output = []
    col_set = set()
    for index, row in df.iterrows():
        output.append(row['First Table Name'] + '.' +
                      row['First Table Foreign Key'] + " = " +
                      row['Second Table Name'] + '.' +
                      row['Second Table Foreign Key'])
        col_set.add(row['First Table Name'] + '.' +
                    row['First Table Foreign Key'])
        col_set.add(row['Second Table Name'] + '.' +
                    row['Second Table Foreign Key'])
    output = ", ".join(output)
    return output, col_set


def quote_field(field_name):
    # 正则表达式判断字段名是否包含空格或特殊字符
    if re.search(r'\W', field_name):
        # 如果匹配到，给字段名添加反引号
        return f"`{field_name}`"
    else:
        # 否则，不做改变
        return field_name


class db_agent:

    def __init__(self, chat_model) -> None:
        self.chat_model = chat_model

    def get_allinfo(self,db_json_dir, db,sqllite_dir,db_dir,tables_info_dir, model):
        db_info, db_col = self.get_db_des(sqllite_dir,db_dir,model)
        foreign_keys = find_foreign_keys_MYSQL_like(tables_info_dir, db)[0]
        all_info = f"Database Management System: SQLite\n#Database name: {db}\n{db_info}\n#Forigen keys:\n{foreign_keys}\n"
        prompt = self.db_conclusion(all_info)
        db_all = self.chat_model.get_ans(prompt)
        all_info = f"{all_info}\n{db_all}\n"

        return all_info, db_col

    def get_complete_table_info(self, conn, table_name, table_df):
        cursor = conn.cursor()
        # 获取列的基本信息
        cursor.execute(f"PRAGMA table_info(`{table_name}`)")
        columns_info = cursor.fetchall()
        df = pd.read_sql_query(f"SELECT * FROM `{table_name}`", conn)
        contains_null = {
            column: df[column].isnull().any()
            for column in df.columns
        }
        contains_duplicates = {
            column: df[column].duplicated().any()
            for column in df.columns
        }
        dic = {}
        for _, row in table_df.iterrows():
            try:
                col_description, val_description = "", ""
                col = str(row.iloc[0]).strip()
                if pd.notna(row.iloc[2]):
                    col_description = re.sub(r'\s+', ' ', str(row.iloc[2]))
                if col_description.strip() == col or col_description.strip(
                ) == "":
                    col_description = ''
                if pd.notna(row.iloc[4]):
                    val_description = re.sub(r'\s+', ' ', str(row.iloc[4]))
                if val_description.strip() == "" or val_description.strip(
                ) == col or val_description == col_description:
                    val_description = ""
                col_description = col_description[:200]
                val_description = val_description[:200]
                dic[col] = col_description, val_description
            except Exception as e:
                print(e)
                dic[col] = "", ""
        # 获取外键信息
        row = list(
            cursor.execute(f"SELECT * FROM `{table_name}` LIMIT 1").fetchall()
            [0])
        for i, col in enumerate(df.columns):
            try:
                vals = df[col].dropna().drop_duplicates().iloc[:3].values
                val_p = []
                for val in vals:
                    try:
                        val_p.append(int(val))
                    except:
                        val_p.append(val)
                if len(vals) == 0:
                    raise ValueError
                row[i] = val_p
            except:
                pass
        # 构建schema表示
        schema_str = f"## Table {table_name}:\nColumn| Column Description| Value Description| Type| 3 Example Value\n"
        columns = {}
        for column, val in zip(columns_info, row):

            column_name, column_type, not_null, default_value, pk = column[1:6]
            tmp_col = column_name.strip()
            column_name = quote_field(column_name)

            schema_str += f"{column_name}| "
            col_des, val_des = dic.get(tmp_col, ["", ""])
            schema_str += f"{col_des}|{val_des}|"
            schema_str += f"{column_type}| "
            include_null = f"{'Include Null' if contains_null[tmp_col] else 'Non-Null'}"
            # schema_str += f"{include_null}| "
            unique = f"{'Non-Unique' if contains_duplicates[tmp_col] else 'Unique'}"
            # schema_str += f"{unique}| "
            if len(str(val)) > 360:  ## ddl展示 索引正常
                val = "<Long text not displayed>"
            columns[f"{table_name}.{column_name}"] = (col_des, val_des,
                                                      column_type,
                                                      include_null, unique,
                                                      str(val))
            schema_str += f"{val}\n"
        return schema_str, columns

    def get_db_des(self,sqllite_dir,db_dir,model):
        conn = sqlite3.connect(sqllite_dir)
        table_dir = os.path.join(db_dir, 'database_description')
        sql = "SELECT name FROM sqlite_master WHERE type='table';"
        cursor = conn.cursor()
        tables = cursor.execute(sql).fetchall()
        db_info = []
        db_col = dict()
        file_list = os.listdir(table_dir)
        files_emb = model.encode(file_list, show_progress_bar=False)
        for table in tables:
            if table[0] == 'sqlite_sequence':
                continue
            files_sim = (files_emb @ model.encode(table[0] + '.csv',
                                                  show_progress_bar=False).T)
            if max(files_sim) > 0.9:
                file = os.path.join(table_dir, file_list[files_sim.argmax()])
            else:
                file = os.path.join(table_dir, table[0] + '.csv')

            try:
                with open(file, 'rb') as f:
                    result = chardet.detect(f.read())
                table_df = pd.read_csv(file, encoding=result['encoding'])
            except Exception as e:
                print(e)
                table_df = pd.DataFrame()
            table_info, columns = self.get_complete_table_info(
                conn, table[0], table_df)
            db_info.append(table_info)
            db_col.update(columns)
        db_info = "\n".join(db_info)
        cursor.close()
        conn.close()

        return db_info, db_col

    def db_conclusion(self, db_info):
        prompt = f"""/* Here is a examples about describe database */
    #Forigen keys: 
    Airlines.ORIGIN = Airports.Code, Airlines.DEST = Airports.Code, Airlines.OP_CARRIER_AIRLINE_ID = Air Carriers.Code
    #Database Description: The database encompasses information related to flights, including airlines, airports, and flight operations.
    #Tables Descriptions:
    Air Carriers: Codes and descriptive information about airlines
    Airports: IATA codes and descriptions of airports
    Airlines: Detailed information about flights 

    /* Here is a examples about describe database */
    #Forigen keys:
    data.ID = price.ID, production.ID = price.ID, production.ID = data.ID, production.country = country.origin
    #Database Description: The database contains information related to cars, including country, price, specifications, Production
    #Tables Descriptions:
    Country: Names of the countries where the cars originate from.
    Price: Price of the car in USD.
    Data: Information about the car's specifications
    Production: Information about car's production.

    /* Describe the following database */
    {db_info}
    Please conclude the database in the following format:
    #Database Description:
    #Tables Descriptions:
    """
        # print(prompt)

        return prompt


class db_agent_string(db_agent):

    def __init__(self, chat_model) -> None:
        super().__init__(chat_model)

    def get_complete_table_info(self, conn, table_name, table_df):
        cursor = conn.cursor()
        # 获取列的基本信息
        cursor.execute(f"PRAGMA table_info(`{table_name}`)")
        columns_info = cursor.fetchall()
        df = pd.read_sql_query(f"SELECT * FROM `{table_name}`", conn)
        contains_null = {
            column: df[column].isnull().any()
            for column in df.columns
        }
        contains_duplicates = {
            column: df[column].duplicated().any()
            for column in df.columns
        }
        dic = {}
        for _, row in table_df.iterrows():
            try:
                col_description, val_description = "", ""
                col = row.iloc[0].strip()
                if pd.notna(row.iloc[2]):
                    col_description = re.sub(r'\s+', ' ', str(row.iloc[2]))
                if col_description.strip() == col or col_description.strip(
                ) == "":
                    col_description = ''
                if pd.notna(row.iloc[4]):
                    val_description = re.sub(r'\s+', ' ', str(row.iloc[4]))
                if val_description.strip() == "" or val_description.strip(
                ) == col or val_description == col_description:
                    val_description = ""
                col_description = col_description[:200]
                val_description = val_description[:200]
                dic[col] = col_description, val_description
            except Exception as e:
                print(e)
                dic[col] = "", ""
        # 获取外键信息
        row = list(
            cursor.execute(f"SELECT * FROM `{table_name}` LIMIT 1").fetchall()
            [0])
        for i, col in enumerate(df.columns):
            try:
                df_tmp=df[col].dropna().drop_duplicates()
                if len(df_tmp)>=3:
                    vals = df_tmp.sample(3).values
                else:
                    vals=df_tmp.values
                val_p = []
                for val in vals:
                    try:
                        val_p.append(int(val))
                    except:
                        val_p.append(val)
                if len(vals) == 0:
                    raise ValueError
                row[i] = val_p
            except:
                pass
        # 构建schema表示
        schema_str = f"## Table {table_name}:\n"
        columns = {}
        for column, val in zip(columns_info, row):
            schema_str_single = ""
            column_name, column_type, not_null, default_value, pk = column[1:6]
            tmp_col = column_name.strip()
            column_name = quote_field(column_name)

            # schema_str_single += f"{column_name}: "
            col_des, val_des = dic.get(tmp_col, ["", ""])
            if col_des != "":
                schema_str_single += f" The column is {col_des}. "
            if val_des != "":
                schema_str_single += f" The values' format are {val_des}. "

            schema_str_single += f"The type is {column_type}, "
            if contains_null[tmp_col]:
                schema_str_single += f"Which inlude Null"
            else:
                schema_str_single += f"Which does not inlude Null"

            if contains_duplicates[tmp_col]:
                schema_str_single += " and is Non-Unique. "
            else:
                schema_str_single += " and is Unique. "

            include_null = f"{'Include Null' if contains_null[tmp_col] else 'Non-Null'}"
            # schema_str_single += f"{include_null}| "
            unique = f"{'Non-Unique' if contains_duplicates[tmp_col] else 'Unique'}"
            # schema_str_single += f"{unique}| "
            if len(str(val)) > 360:  ## ddl展示 索引正常
                val="<Long text>"
                schema_str_single+= f"Values format: <Long text>"
            elif  type(val) is not list or len(val)<3 :
                schema_str_single+= f"Value of this column must in: {val}"
            else:
                schema_str_single += f"Values format like: {val}"
            schema_str += f"{column_name}: {schema_str_single}\n"
            columns[f"{table_name}.{column_name}"] = (schema_str_single,
                                                      col_des, val_des,
                                                      column_type,
                                                      include_null, unique,
                                                      str(val))
        return schema_str, columns
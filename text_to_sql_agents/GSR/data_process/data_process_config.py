API_KEYS = ""

model_openai = "gpt-4o"

DATA_PATH = "../data"

INPUT_PROMPT = "###Input:\n{}\n\n###Response:"

INSTRUCTION_PROMPT = """\
I want you to act as a SQL terminal in front of an example database, \
you need only to return the sql command to me.Below is an instruction that describes a task, \
Write a response that appropriately completes the request.\n
##Instruction:\n{}\n"""

SQL_DATA_INFO = [
    {
        "data_source": "dev_20240627",      # set
        "file": ["dev.json"],               # set
        "tables_file": "dev_tables.json",   # set
        "database_name": "dev_database",    # set
        "db_id_name": "db_id",
        "output_name": "SQL",
    }
]

DATABASE_PATH = "database/dev_20240627/dev_databases"   # set

PRESQL_HINT_PROMPT = ("You are a database expert. Based on the following sections: ###Database Schema, ###Input, ###Hint, and ###Logic Clause, "
                               "generate the SQL query that meets the requirements of ###Input. Each section provides specific information:\n\n"
                               "###Database Schema: Details the structure of the database, including tables and columns.\n"
                               "###Input: Specifies the data the user wants to query, including required columns and conditions.\n"
                               "###Hint: Provides additional context or constraints related to the ###Input. Some reference information for you to complete ###Input.\n"
                               "###Logic Clause: Offers further explanation to clarify the query requirements.\n\n"
                               "Goal: 1. Correctly understand the requirements of ###Input based on ###Logic Clause.\n"
                               "2. Be sure to use the hints given in ###Hint, then determine which part of ###Input the hints are used to complete, "
                               "and write SQL that combines the contents of ###Hint and ###Input, and do not write anything that is not mentioned in ###Input.\n"
                               "3. Using SQLite syntax, write a single-line SQL query that selects only the columns required by ###Input.\n\n"
                               "Output Format:\n\nOnly return the SQL statement as a single line, following this format:\n\n"
                               "###SQL: SELECT song_name , song_release_year FROM singer ORDER BY age LIMIT 1; ###END")


PRESQL_PROMPT = ("You are a database expert. Based on the following sections: ###Database Schema, ###Input, and ###Logic Clause, "
                               "generate the SQL query that meets the requirements of ###Input. Each section provides specific information:\n\n"
                               "###Database Schema: Details the structure of the database, including tables and columns.\n"
                               "###Input: Specifies the data the user wants to query, including required columns and conditions.\n"
                               "###Logic Clause: Offers further explanation to clarify the query requirements.\n\n"
                               "Goal: 1. Correctly understand the requirements of ###Input based on ###Logic Clause.\n"
                               "2. Using SQLite syntax, write a single-line SQL query that selects only the columns required by ###Input.\n\n"
                               "Output Format:\n\nOnly return the SQL statement as a single line, following this format:\n\n"
                               "###SQL: SELECT song_name , song_release_year FROM singer ORDER BY age LIMIT 1; ###END")


SECOND_SQL_PROMPT = """You are a database expert. Please help me check the Pre-SQL based on ###Input, ###Pre-SQL and ###Value Examples. Please follow the steps below:
1. Pay close attention to the column_description (if provided) for each column in the ###Value Examples. Explicitly write out the column_description, analyze them, and check if the correct columns are being used in the current SQL.
2. Pay close attention to the value_description (if provided) and the value_sample for each column. Explicitly write out the content of the specific value_description and the value in the value_sample.
3. Please check that the value written in the SQL condition exists in the value example, if there may not be a corresponding value in the current column, it is possible that the wrong column is being used, consider whether other columns could complete the ###Input. When performing this step, please refer to the ###Value example.
4. Check the values used in the conditional section of the SQL, compare the values in the SQL with the values in the value_sample displayed, and make sure that the values are case-accurate (this is very important).
5. If you identify any issues with the current SQL after your analysis, please help correct it. While fixing the SQL, ensure that it follows SQLite syntax. If no issues are found, do not make any changes, and provide the original SQL as is.
6. If the SQL contains arithmetic operations, explicitly identify the arithmetic operation parts and force the use of the CAST function to convert those parts to a floating-point type.
7. Provide the final SQL with or without corrections based on your analysis. 
8. Please place the final SQL on the last line and write the SQL in a single line following the format below, without adding any line breaks in the SQL and without using any other format:
###SQL: SELECT song_name, song_release_year FROM singer ORDER BY age LIMIT 1; ###END"""

SECOND_SQL_HINT_PROMPT = """You are a database expert. Please help me check the Pre-SQL based on ###Input, ###Hint, ###Pre-SQL and ###Value Examples. Please follow the steps below:
1. Pay close attention to the column_description (if provided) for each column in the ###Value Examples. Explicitly write out the column_description, analyze them, and check if the correct columns are being used in the current SQL.
2. Pay close attention to the value_description (if provided) and the value_sample for each column. Explicitly write out the content of the specific value_description and the value in the value_sample.
3. Please check that the value written in the SQL condition exists in the value example, if there may not be a corresponding value in the current column, it is possible that the wrong column is being used, consider whether other columns could complete the ###Input. When performing this step, please refer to the ###Value example and do not rely on the information in the ###Hint.
4. Check the values used in the conditional section of the SQL, compare the values in the SQL with the values in the value_sample displayed, and make sure that the values are case-accurate (this is very important).
5. If you identify any issues with the current SQL after your analysis, please help correct it. While fixing the SQL, ensure that it follows SQLite syntax. If no issues are found, do not make any changes, and provide the original SQL as is.
6. If the SQL contains arithmetic operations, explicitly identify the arithmetic operation parts and force the use of the CAST function to convert those parts to a floating-point type.
7. Provide the final SQL with or without corrections based on your analysis. 
8. Please place the final SQL on the last line and write the SQL in a single line following the format below, without adding any line breaks in the SQL and without using any other format:
###SQL: SELECT song_name, song_release_year FROM singer ORDER BY age LIMIT 1; ###END"""
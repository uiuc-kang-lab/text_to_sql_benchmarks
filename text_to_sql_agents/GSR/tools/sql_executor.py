import json
import multiprocessing
import re
import sqlite3

import pandas as pd

from .extractor import extractor, text_keyword_column_value_extractor
from .value_condition_check import value_condition_check
from .similarity_search import research

with open('../data/mapping/all_mappings.json', 'r') as f:
    all_mappings = json.load(f)

def update_value_sample(data, table_name, column_name, new_sample):     # This function is used to replace the content of those who have used the vector database for the value example lookup, mainly to replace the content of the string
    # Optimised regular expression to ensure that it matches the -value_sample part and pinpoints the exact location
    pattern = (
        rf"(-Table: {re.escape(table_name)}\n\t.*?-column: {re.escape(column_name)}\n\t\t.*?-value_sample: )(\[.*?\])( \()"
    )

    # Convert new_sample list to string, keep \xa0
    new_sample = "[" + ", ".join(new_sample) + "]"

    # Creating new -value_sample content
    replacement = rf"\1{new_sample}\3"

    # Replaces the -value_sample content, but retains the (Total records, Unique values) information that follows
    updated_data = re.sub(
        pattern,
        replacement,
        data,
        flags=re.DOTALL
    )
    return updated_data

def value_example_extractor(db_file, pre_sql, text_input):

    # Database name
    database_name = db_file.split("/")[-2]

    # Similarity search algorithms can use flags, available set to 1, not available set to 0
    similar_use_flag = 0;

    # No error message flag, no error set to 1, with error set to 0
    no_error_message_flag = 1;

    # Used to save error messages
    error_messages = ""

    # Connecting to database files
    conn = sqlite3.connect(db_file)
    cursor = conn.cursor()

    table_schema = extractor(pre_sql)

    # Regular expression matching pattern
    table_pattern = r'Table (\w+):\s*columns:([^}]+)'
    matches = re.findall(table_pattern, table_schema)

    # Using Dictionaries to Store Results
    table_dict = {}

    # Save the columns that do not show all the examples of values, and the tables that correspond to the columns.
    no_all_value_examples_columnsWithTables = []

    for match in matches:
        table_name = match[0]
        # Extract all column names using regular expressions separated by commas
        columns_pattern = r'"([^"]+)"'
        table_columns = re.findall(columns_pattern, match[1])  # Extract Column Name
        # Save to Dictionary
        table_dict[table_name] = table_columns

    value_all_info = ""     # Value information for all tables
    value_one_info = ""     # Value information for a single table
    error_each_table_column_count = 0  # Number of columns used to record errors per table
    error_total_column_count = 0  # Number of columns used to record the total number of errors

    for idx, (table_name, columns) in enumerate(table_dict.items()):
        value_one_info = ""
        value_one_info += "-Table: " + table_name
        for index, column in enumerate(columns):
            try:
                # Number of types of columns
                sql_command_1 = "SELECT COUNT(DISTINCT `" + str(column) + "`) FROM `" + str(table_name) + "`;"
                # Total number of records in column
                sql_command_2 = "SELECT COUNT(`" + str(column) + "`) FROM `" + str(table_name) + "`;"
                # The value of all categories of the column
                sql_command_3 = "SELECT DISTINCT `" + str(column) + "` FROM `" + str(table_name) + "`;"
                # columns of all kinds of values, limiting the return to 3
                sql_command_4 = "SELECT DISTINCT `" + str(column) + "` FROM `" + str(table_name) + "` LIMIT 3;"
                # Existence test for null values
                sql_command_null_check = "SELECT DISTINCT `" + str(column) + "` FROM `" + str(table_name) + "` WHERE `" + str(column) + "` IS NULL"

                cursor.execute(sql_command_1)
                result_1 = cursor.fetchall()        # Unique values
                cursor.execute(sql_command_2)
                result_2 = cursor.fetchall()        # Total records

                unique_values = result_1[0][0]      # Unique values
                total_record = result_2[0][0]       # Total records

                if int(result_1[0][0]) < 50 or (int(result_1[0][0]) < 100 and int(result_1[0][0]) < int(result_2[0][0])/10):
                    cursor.execute(sql_command_3)
                    result_3 = cursor.fetchall()

                    value = []
                    for row in result_3:
                        value.append(row[0])
                else:
                    similar_use_flag = 1;   # Setting the similarity search algorithm use flag to 1 indicates that a similarity search algorithm may be required
                    no_all_value_examples_columnsWithTables.append([str(column),str(table_name),False])    # When the front column cannot show all the values, add them to the list.

                    cursor.execute(sql_command_4)
                    result_4 = cursor.fetchall()
                    value = []
                    for row in result_4:
                        value.append(row[0])

                    # Checks if there is a null value in the current column.
                    cursor.execute(sql_command_null_check)
                    null_value = cursor.fetchall()
                    if null_value:
                        value.append(null_value[0][0])

                table_database = db_file.rsplit('/',2)[1] + "/" + table_name.lower() + ".csv"
                column_description = all_mappings[table_database]['column_description_mapping'].get(column)
                value_description = all_mappings[table_database]['value_description_mapping'].get(column)

                # value_all_info information
                value_one_info += "\n\t"

                column_info = "-column: " + column
                if column_description is not None and not pd.isna(column_description):
                    column_description_info = "-column_description: " + column_description
                    value_one_info += column_info + "\n\t\t" + column_description_info + "\n\t\t"
                else:
                    value_one_info += column_info + "\n\t\t"
                value_sample_info = "-value_sample: " + str(value) + " (Total records: " + str(total_record) + ", Unique values: " + str(unique_values) +")"
                if value_description is not None and not pd.isna(value_description):
                    value_description_info = "-value_description: \"\"\"" + value_description + "\"\"\""
                    value_one_info += value_sample_info + "\n\t\t" + value_description_info
                else:
                    value_one_info += value_sample_info

            except Exception as e:
                no_error_message_flag = 0;  # Set the no-error-message flag to 0 to indicate that the similarity search algorithm will not be used in this function call if there is an error message

                error_each_table_column_count += 1
                error_total_column_count += 1

                error_messages += f"{error_total_column_count}. An error occurred while executing SQL for table '{table_name}' and column '{column}': {e}\n"

        if error_each_table_column_count == len(columns):  # The number of erroneous columns in the current table is equal to the number of relevant columns in the current table
            value_one_info = ""
        elif idx == len(table_dict) - 1:   # The number of erroneous columns is less than the number of relevant columns in the current table, and it is the last table.
            value_all_info += value_one_info
        else:                               # The number of incorrect columns is less than the number of relevant columns in the current table Also, it is not the last table.
            value_all_info += value_one_info + "\n\n"

        error_each_table_column_count = 0

    if similar_use_flag == 1 and no_error_message_flag == 1:
        for item in no_all_value_examples_columnsWithTables:
            item[2] = value_condition_check(pre_sql, item[0], item[1])      # Determine if the column that cannot return all the value examples is a column that involves a value judgement
        current_value_query_columnsWithTables = [item for item in no_all_value_examples_columnsWithTables if item[2] == True]         # All columns in the value section of the current SQL that do not return all of the value examples and the corresponding tables
        if current_value_query_columnsWithTables:     # If the current list is not empty, execute
            current_value_query_columns = [item[0] for item in current_value_query_columnsWithTables]
            keyword_column_value_dict = text_keyword_column_value_extractor(text_input, pre_sql, current_value_query_columns)  # Here we need to consider that after taking the keys from the dictionary as a list, there may be duplicate values, i.e. the same column from different tables
            replace_table_column_value_examples = []
            try:
                for column, keyword in keyword_column_value_dict.items():
                    column_from_table = [item[1] for item in current_value_query_columnsWithTables if item[0] == str(column)]
                    for table_name in column_from_table:
                        similar_examples = research(db_file, table_name, column, keyword)
                        replace_table_column_value_examples.append([table_name, column, similar_examples])
                for info in replace_table_column_value_examples:
                    if info[2] != []:
                        value_all_info = update_value_sample(value_all_info, info[0], info[1], info[2])
            except Exception as e:
                print(f"Unexpected error in processing columns and keywords: {e}")

    conn.close()

    return value_all_info, error_messages, table_dict


def value_example_extractor_masked_extra_schema(db_file, masked_schema, pre_value_all_info, pre_current_table_dict):

    # Database name
    database_name = db_file.split("/")[-2]

    # Similarity search algorithms can use flags, available set to 1, not available set to 0
    similar_use_flag = 0;

    # No error message flag, no error set to 1, with error set to 0
    no_error_message_flag = 1;

    # Used to save error messages
    error_messages = ""

    # Connecting to database files
    conn = sqlite3.connect(db_file)
    cursor = conn.cursor()

    # Save the columns that do not show all the examples of values, and the tables that correspond to the columns.
    no_all_value_examples_columnsWithTables = []

    value_all_info = pre_value_all_info + "\n\n"     # Value information for all tables
    value_one_info = ""     # Value information for a single table
    error_each_table_column_count = 0  # Number of columns used to record errors per table
    error_total_column_count = 0  # Number of columns used to record the total number of errors

    for idx, (table_name, columns) in enumerate(masked_schema.items()):
        value_one_info = ""
        value_one_info += "-Table: " + table_name
        if pre_current_table_dict.get(table_name):      # If the newly appended column belongs to a table that already exists in pre_dict
            replace_column_flag = 1     # Replacement mode
        else:
            replace_column_flag = 0     # Non-replacement mode
        for index, column in enumerate(columns):
            try:
                # Number of types of columns
                sql_command_1 = "SELECT COUNT(DISTINCT `" + str(column) + "`) FROM `" + str(table_name) + "`;"
                # Total number of records in column
                sql_command_2 = "SELECT COUNT(`" + str(column) + "`) FROM `" + str(table_name) + "`;"
                # The value of all categories of the column
                sql_command_3 = "SELECT DISTINCT `" + str(column) + "` FROM `" + str(table_name) + "`;"
                # columns of all kinds of values, limiting the return to 3
                sql_command_4 = "SELECT DISTINCT `" + str(column) + "` FROM `" + str(table_name) + "` LIMIT 3;"
                # Existence test for null values
                sql_command_null_check = "SELECT DISTINCT `" + str(column) + "` FROM `" + str(table_name) + "` WHERE `" + str(column) + "` IS NULL"

                cursor.execute(sql_command_1)
                result_1 = cursor.fetchall()        # Unique values
                cursor.execute(sql_command_2)
                result_2 = cursor.fetchall()        # Total records

                unique_values = result_1[0][0]      # Unique values
                total_record = result_2[0][0]       # Total records

                if int(result_1[0][0]) < 50 or (int(result_1[0][0]) < 100 and int(result_1[0][0]) < int(result_2[0][0])/10):
                    cursor.execute(sql_command_3)
                    result_3 = cursor.fetchall()

                    value = []
                    for row in result_3:
                        value.append(row[0])

                else:
                    similar_use_flag = 1;   # Setting the similarity search algorithm use flag to 1 indicates that a similarity search algorithm may be required
                    no_all_value_examples_columnsWithTables.append([str(column),str(table_name),False])    # When the front column cannot show all the values, add them to the list

                    cursor.execute(sql_command_4)
                    result_4 = cursor.fetchall()
                    value = []
                    for row in result_4:
                        value.append(row[0])

                    # Checks if there is a null value in the current column.
                    cursor.execute(sql_command_null_check)
                    null_value = cursor.fetchall()
                    if null_value:
                        value.append(null_value[0][0])

                table_database = db_file.rsplit('/',2)[1] + "/" + table_name.lower() + ".csv"
                column_description = all_mappings[table_database]['column_description_mapping'].get(column)
                #value_description = all_mappings[table_database]['value_description_mapping'].get(column)

                value_one_info += "\n\t"

                column_info = "-column: " + column
                if column_description is not None and not pd.isna(column_description):
                    column_description_info = "-column_description: " + column_description
                    value_one_info += column_info + "\n\t\t" + column_description_info + "\n\t\t"
                else:
                    value_one_info += column_info + "\n\t\t"
                value_sample_info = "-value_sample: " + str(value) + " (Total records: " + str(total_record) + ", Unique values: " + str(unique_values) +")"
                # if value_description is not None and not pd.isna(value_description):
                #     value_description_info = "-value_description: \"\"\"" + value_description + "\"\"\""
                #     value_one_info += value_sample_info + "\n\t\t" + value_description_info
                # else:
                value_one_info += value_sample_info

            except Exception as e:
                no_error_message_flag = 0;  # Set the no-error-message flag to 0 to indicate that the similarity search algorithm will not be used in this function call if there is an error message

                error_each_table_column_count += 1
                error_total_column_count += 1
                error_messages += f"{error_total_column_count}. An error occurred while executing SQL for table '{table_name}' and column '{column}': {e}\n"

        if error_each_table_column_count == len(columns):  # The number of erroneous columns in the current table is equal to the number of relevant columns in the current table
            value_one_info = ""
        elif replace_column_flag:
            replacement_info = "-Table: " + table_name
            value_all_info = value_all_info.replace(replacement_info, value_one_info)
            if idx == len(masked_schema) - 1:   # The number of erroneous columns is less than the number of relevant columns in the current table, and it is the last table.
                if value_all_info.endswith("\n\n"):
                    value_all_info = value_all_info[:-2]
        elif idx == len(masked_schema) - 1:   # The number of erroneous columns is less than the number of relevant columns in the current table, and it is the last table.
            value_all_info += value_one_info
        else:                               # The number of incorrect columns is less than the number of relevant columns in the current table Also, it is not the last table.
            value_all_info += value_one_info + "\n\n"

        error_each_table_column_count = 0

    conn.close()

    error_messages = ""

    return value_all_info, error_messages



def execute_sql_in_process(db_file, sql, result_queue):
    try:

        conn = sqlite3.connect(db_file, timeout = 20)
        cursor = conn.cursor()

        cursor.execute(sql)
        result = cursor.fetchall()

        result_queue.put((result, ""))
    except Exception as e:
        result_queue.put((None, f"An error occurred while executing SQL: {e}"))

    finally:
        try:
            cursor.close()
            conn.close()
        except Exception as close_error:
            result_queue.put((None, f"An error occurred while closing the connection: {close_error}"))

def one_sql_execute(db_file, sql, timeout = 30):
    # Queues for storing results
    result_queue = multiprocessing.Queue()

    # Start a new process to execute the SQL
    process = multiprocessing.Process(target=execute_sql_in_process, args=(db_file, sql, result_queue))
    process.start()

    # Wait for the process to complete within the specified timeout period
    process.join(timeout)

    # Check if there are results in the queue
    if not result_queue.empty():
        result, error_messages = result_queue.get()
        return result, error_messages

    # Check if the process is still running (timeout not completed)
    if process.is_alive():
        # Termination of sub-processes
        process.terminate()
        process.join()
        return None, f"SQL execution timed out after {timeout} seconds."

    # Getting results from the queue
    result, error_messages = result_queue.get()

    return result, error_messages

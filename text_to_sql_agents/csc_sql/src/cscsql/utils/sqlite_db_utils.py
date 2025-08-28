import os
import random
import sqlite3
import traceback
from typing import List, Dict, Tuple, Union, Any, Optional

from func_timeout import func_set_timeout, FunctionTimedOut, func_timeout

from cscsql.utils.string_utils import StringUtils
from cscsql.utils.logger_utils import logger

__all__ = [
    "execute_sql",
    "SqliteDbUtils"
]


# execute predicted sql with a time limitation
@func_set_timeout(2000)
def execute_sql(cursor, sql: str):
    cursor.execute(sql)

    return cursor.fetchall()


def execute_sql_with_mode(db_path: str, sql: str, fetch: Union[str, int] = "all") -> Any:
    """
    Executes an SQL query on a database and fetches results.

    Args:
        db_path (str): The path to the database file.
        sql (str): The SQL query to execute.
        fetch (Union[str, int]): How to fetch the results. Options are "all", "one", "random", or an integer.

    Returns:
        Any: The fetched results based on the fetch argument.

    Raises:
        Exception: If an error occurs during SQL execution.
    """
    try:
        with sqlite3.connect(db_path) as conn:
            cursor = conn.cursor()
            cursor.execute(sql)
            if fetch == "all":
                return cursor.fetchall()
            elif fetch == "one":
                return cursor.fetchone()
            elif fetch == "random":
                samples = cursor.fetchmany(10)
                return random.choice(samples) if samples else []
            elif isinstance(fetch, int):
                return cursor.fetchmany(fetch)
            else:
                raise ValueError("Invalid fetch argument. Must be 'all', 'one', 'random', or an integer.")
    except Exception as e:
        print(f"Error in execute_sql: {e}\nSQL: {sql}")
        raise e


# execute predicted sql with a long time limitation (for building content index)
@func_set_timeout(2000)
def execute_sql_long_time_limitation(cursor, sql):
    cursor.execute(sql)

    return cursor.fetchall()


class SqliteDbUtils(object):
    """
    文件工具类
    """

    SQL_GET_ALL_TABLES = "SELECT name FROM sqlite_master WHERE type='table';"
    SQL_GET_TABLE_COLUMN = "PRAGMA table_info(`{table_name}`);"
    SQL_GET_TABLE_FOREIGN_KEYS = "PRAGMA foreign_key_list(`{table_name}`);"
    SQL_GET_TABLE_SAMPLE_WITH_LIMIT = "SELECT * FROM `{table_name}` LIMIT {sample_limit};"
    SQL_GET_COLUMN_DISTINCT_CONTENT_TOTAL = "SELECT count(distinct {column_name}) as total FROM `{table_name}`;"
    SQL_GET_COLUMN_DISTINCT_CONTENT = "SELECT {column_name}, count(1) as total FROM `{table_name}` group by {column_name} order by total desc limit {sample_limit}; "
    SQL_GET_COLUMN_CONTENT_BY_ENTITY = "SELECT distinct {column_name} FROM `{table_name}` where lower({column_name}) = lower('{entity_name}'); "
    SQL_GET_COLUMN_NOT_NULL_DISTINCT = "SELECT DISTINCT `{column_name}` FROM `{table_name}` WHERE `{column_name}` IS NOT NULL"

    def init(self):
        pass

    @staticmethod
    def execute_sql(db_path: str, sql: str, fetch: Union[str, int] = "all",
                    meta_time_out=30.0) -> Any:
        """
        Executes an SQL query on a database and fetches results.

        Args:
            db_path (str): The path to the database file.
            sql (str): The SQL query to execute.
            fetch (Union[str, int]): How to fetch the results. Options are "all", "one", "random", or an integer.

        Returns:
            Any: The fetched results based on the fetch argument.

        Raises:
            Exception: If an error occurs during SQL execution.
        """
        try:
            res = func_timeout(meta_time_out, execute_sql_with_mode,
                               args=(db_path, sql, fetch))
            return res
        except FunctionTimedOut:
            logger.error(f"Error in execute_sql: timeout {meta_time_out}\nSQL: {sql}")
            result = [(f'timeout',)]
            return result
        except Exception as e:
            logger.error(f"Error in execute_sql: {e}\nSQL: {sql}")
            raise e

    @staticmethod
    def get_cursor_from_path(sqlite_path: str):
        """
         get the database cursor for a sqlite database path

        """
        try:
            if not os.path.exists(sqlite_path):
                print("Opening a new connection %s" % sqlite_path)
            connection = sqlite3.connect(sqlite_path, check_same_thread=False)
        except Exception as e:
            print(sqlite_path)
            raise e
        connection.text_factory = lambda b: b.decode(errors="ignore")
        cursor = connection.cursor()
        return cursor

    @staticmethod
    def run_sql(cursor, sql: str, db_uri: str = None) -> List:
        if cursor is None and db_uri is None:
            raise Exception("cursor is required")
        if cursor is None:
            cursor = SqliteDbUtils.get_cursor_from_path(db_uri)
        results = []
        try:
            results = execute_sql(cursor=cursor, sql=sql)
        except Exception as e:
            traceback.print_exc()
            logger.error(f"执行sql出错：{sql} - {db_uri}")
        return results

    @staticmethod
    def get_all_table_names(cursor, clean_chess=False) -> list[str]:
        results = SqliteDbUtils.run_sql(cursor, sql=SqliteDbUtils.SQL_GET_ALL_TABLES)
        table_names = [item[0] for item in results]
        if clean_chess:
            table_names = [StringUtils.clean_chess_str(name)
                           for name in table_names if name != "sqlite_sequence"]

        return table_names

    @staticmethod
    def get_db_all_tables(db_path: str) -> List[str]:
        cursor = SqliteDbUtils.get_cursor_from_path(db_path)
        table_names = SqliteDbUtils.get_all_table_names(cursor, clean_chess=True)
        return table_names

    @staticmethod
    def get_table_columns(cursor, table_name: str) -> List:
        sql = SqliteDbUtils.get_sql_table_info(table_name)
        results = SqliteDbUtils.run_sql(cursor, sql)
        return results

    @staticmethod
    def get_sql_table_info(table_name):
        sql = SqliteDbUtils.SQL_GET_TABLE_COLUMN.format(table_name=table_name)
        return sql

    @staticmethod
    def get_table_foreign_keys(cursor, table_name: str) -> List:
        sql = SqliteDbUtils.SQL_GET_TABLE_FOREIGN_KEYS.format(table_name=table_name)
        results = SqliteDbUtils.run_sql(cursor, sql)
        return results

    @staticmethod
    def get_table_columns_by_list(cursor, given_tables: list[str]) -> List:
        table_names = SqliteDbUtils.get_all_table_names(cursor=cursor)
        all_columns = []
        for given_table in given_tables:
            for table_name in table_names:
                if table_name == given_table:
                    columns = SqliteDbUtils.get_table_columns(cursor=cursor, table_name=table_name)
                    all_columns.append(columns)
                    break
        return all_columns

    @staticmethod
    def get_all_column_names(cursor, given_tables: list[str]) -> list[list[str]]:
        columns = SqliteDbUtils.get_table_columns_by_list(cursor=cursor, given_tables=given_tables)
        column_names = []
        for one_table in columns:
            column_names.append([column[1] for column in one_table])
        return column_names

    @staticmethod
    def get_table_column_names_v0(cursor, table_name: str) -> list[str]:
        column_names = SqliteDbUtils.get_all_column_names(cursor=cursor, given_tables=[table_name])
        if len(column_names) > 0:
            column_names = column_names[0]
        return column_names

    @staticmethod
    def get_table_column_names(cursor, table_name: str, clean_chess=False) -> list[str]:
        result = SqliteDbUtils.get_table_columns(cursor=cursor, table_name=table_name)
        column_names = [column[1] for column in result]
        if clean_chess:
            column_names = [StringUtils.clean_chess_str(name) for name in column_names]

        return column_names

    @staticmethod
    def get_table_all_columns(db_path: str, table_name: str) -> List[str]:
        cursor = SqliteDbUtils.get_cursor_from_path(db_path)
        column_names = SqliteDbUtils.get_table_column_names(cursor, table_name=table_name,
                                                            clean_chess=True)
        return column_names

    @staticmethod
    def get_db_table_and_columns(cursor, db_path=None, clean_chess=True) -> Dict[str, List[str]]:
        """
        Retrieves the schema of the database.

        :param cursor:
        :param db_path:
        :param clean_chess:
        :return:  A dictionary mapping table names to lists of column names.
        """
        if cursor is None and db_path:
            cursor = SqliteDbUtils.get_cursor_from_path(db_path)

        try:
            table_names = SqliteDbUtils.get_all_table_names(cursor=cursor, clean_chess=clean_chess)
            result = {table_name: SqliteDbUtils.get_table_column_names(cursor, table_name=table_name,
                                                                       clean_chess=clean_chess)
                      for table_name in table_names}
            return result
        except Exception as e:
            logger.error(f"Error in get_db_schema: {e}")
            raise e

    @staticmethod
    def get_all_primary_keys(cursor, given_tables: list[str]) -> list[list[str]]:
        columns = SqliteDbUtils.get_table_columns_by_list(cursor=cursor, given_tables=given_tables)
        column_names = []
        for one_table in columns:
            column_names.append([column[1] for column in one_table if column[5] > 0])
        return column_names

    @staticmethod
    def get_number_of_columns(cursor, given_tables: list[str]) -> list[int]:
        columns = SqliteDbUtils.get_table_columns_by_list(cursor=cursor, given_tables=given_tables)
        number_of_columns = [len(item) for item in columns]
        return number_of_columns

    @staticmethod
    def check_sql_executable(generated_sql, db):
        if generated_sql.strip() == "":
            return "Error: empty string"
        try:
            cursor = SqliteDbUtils.get_cursor_from_path(db)
            # use `EXPLAIN QUERY PLAN` to avoid actually executing
            execute_sql(cursor, "EXPLAIN QUERY PLAN " + generated_sql)
            execution_error = None
        except FunctionTimedOut as fto:
            print("SQL execution time out error: {}.".format(fto))
            execution_error = "SQL execution times out."
        except Exception as e:
            print("SQL execution runtime error: {}.".format(e))
            execution_error = str(e)

        return execution_error

    @staticmethod
    def is_number(s):
        try:
            float(s)
            return True
        except ValueError:
            return False

    @staticmethod
    def detect_special_char(name):
        for special_char in ['(', '-', ')', ' ', '/']:
            if special_char in name:
                return True

        return False

    @staticmethod
    def add_quotation_mark(s):
        return "`" + s + "`"

    @staticmethod
    def get_column_contents(column_name, table_name, cursor, limit_total=5, max_len=25):
        select_column_sql = (f"SELECT DISTINCT `{column_name}` FROM `{table_name}`"
                             f" WHERE `{column_name}` IS NOT NULL LIMIT {limit_total};")
        results = execute_sql_long_time_limitation(cursor, select_column_sql)
        column_contents = [str(result[0]).strip() for result in results]
        # remove empty and extremely-long contents
        column_contents = [content for content in column_contents if len(content) != 0 and len(content) <= max_len]

        return column_contents

    @staticmethod
    def get_db_schema_sequence(schema):
        schema_sequence = "database schema :\n"
        for table in schema["schema_items"]:
            table_name, table_comment = table["table_name"], table["table_comment"]
            if SqliteDbUtils.detect_special_char(table_name):
                table_name = SqliteDbUtils.add_quotation_mark(table_name)

            # if table_comment != "":
            #     table_name += " ( comment : " + table_comment + " )"

            column_info_list = []
            for column_name, column_type, column_comment, column_content, pk_indicator in \
                    zip(table["column_names"], table["column_types"], table["column_comments"],
                        table["column_contents"],
                        table["pk_indicators"]):
                if SqliteDbUtils.detect_special_char(column_name):
                    column_name = SqliteDbUtils.add_quotation_mark(column_name)
                additional_column_info = []
                # column type
                additional_column_info.append(column_type)
                # pk indicator
                if pk_indicator != 0:
                    additional_column_info.append("primary key")
                # column comment
                if column_comment != "":
                    additional_column_info.append("comment : " + column_comment)
                # representive column values
                if len(column_content) != 0:
                    additional_column_info.append("values : " + " , ".join(column_content))

                column_info_list.append(
                    table_name + "." + column_name + " ( " + " | ".join(additional_column_info) + " )")

            schema_sequence += "table " + table_name + " , columns = [ " + " , ".join(column_info_list) + " ]\n"

        if len(schema["foreign_keys"]) != 0:
            schema_sequence += "foreign keys :\n"
            for foreign_key in schema["foreign_keys"]:
                for i in range(len(foreign_key)):
                    if SqliteDbUtils.detect_special_char(foreign_key[i]):
                        foreign_key[i] = SqliteDbUtils.add_quotation_mark(foreign_key[i])
                schema_sequence += "{}.{} = {}.{}\n".format(foreign_key[0], foreign_key[1], foreign_key[2],
                                                            foreign_key[3])
        else:
            schema_sequence += "foreign keys : None\n"

        return schema_sequence.strip()

    @staticmethod
    def get_matched_content_sequence(matched_contents):
        content_sequence = ""
        if len(matched_contents) != 0:
            content_sequence += "matched contents :\n"
            for tc_name, contents in matched_contents.items():
                table_name = tc_name.split(".")[0]
                column_name = tc_name.split(".")[1]
                if SqliteDbUtils.detect_special_char(table_name):
                    table_name = SqliteDbUtils.add_quotation_mark(table_name)
                if SqliteDbUtils.detect_special_char(column_name):
                    column_name = SqliteDbUtils.add_quotation_mark(column_name)

                content_sequence += table_name + "." + column_name + " ( " + " , ".join(contents) + " )\n"
        else:
            content_sequence = "matched contents : None"

        return content_sequence.strip()

    @staticmethod
    def get_table_sample_rows(cursor, table_name: str, sample_limit=3, db_uri: str = None):
        # Fetch sample data
        max_sample = 1000
        sql = SqliteDbUtils.SQL_GET_TABLE_SAMPLE_WITH_LIMIT.format(table_name=table_name,
                                                                   sample_limit=max_sample)
        sample_rows = SqliteDbUtils.run_sql(cursor, sql=sql, db_uri=db_uri)
        if len(sample_rows) > sample_limit and sample_limit < max_sample:
            sample_rows = random.sample(sample_rows, sample_limit)
        return sample_rows

    @staticmethod
    def get_column_distinct_content_total(cursor, table_name: str, column_name: str):
        sql = SqliteDbUtils.SQL_GET_COLUMN_DISTINCT_CONTENT_TOTAL.format(table_name=table_name,
                                                                         column_name=column_name)
        result = SqliteDbUtils.run_sql(cursor, sql=sql)
        if result is not None and len(result) > 0:
            diff_total = result[0][0]
        else:
            diff_total = 0

        return diff_total

    @staticmethod
    def get_column_distinct_content(cursor, table_name: str, column_name: str, sample_limit=100) -> List[List]:
        sql = SqliteDbUtils.SQL_GET_COLUMN_DISTINCT_CONTENT.format(table_name=table_name,
                                                                   column_name=column_name,
                                                                   sample_limit=sample_limit
                                                                   )
        result = SqliteDbUtils.run_sql(cursor, sql=sql)
        diff_content = []
        for item in result:
            diff_content.append([item[0], item[1]])

        return diff_content

    @staticmethod
    def get_table_column_diff_content(cursor, table_name: str,
                                      column_name: str, sample_limit=10) -> Tuple[int, List[List]]:
        """
        获取字段不同类型总量

        :param cursor:
        :param table_name:
        :param column_name:
        :param sample_limit:
        :return:
        """
        diff_total = SqliteDbUtils.get_column_distinct_content_total(cursor=cursor,
                                                                     table_name=table_name,
                                                                     column_name=column_name)
        diff_content = []
        if diff_total > 0:
            diff_content = SqliteDbUtils.get_column_distinct_content(cursor=cursor,
                                                                     table_name=table_name,
                                                                     column_name=column_name,
                                                                     sample_limit=sample_limit)
        return diff_total, diff_content

    @staticmethod
    def get_column_content_by_entity_same(cursor, table_name: str, column_name: str, entity: str) -> List[str]:
        sql = SqliteDbUtils.SQL_GET_COLUMN_CONTENT_BY_ENTITY.format(table_name=table_name,
                                                                    column_name=column_name,
                                                                    entity_name=entity
                                                                    )
        # print(sql)
        result = SqliteDbUtils.run_sql(cursor, sql=sql)
        diff_content = []
        for item in result:
            diff_content.append(item[0])

        return diff_content

    @staticmethod
    def skip_column(column_name: str, column_values: List[str]) -> bool:
        """
        Determines whether to skip processing a column based on its values.

        Args:
            column_name (str): The name of the column.
            column_values (List[str]): The list of values in the column.

        Returns:
            bool: True if the column should be skipped, False otherwise.
        """
        if "name" in column_name.lower():
            return False
        sum_of_lengths = sum(len(value) for value in column_values)
        average_length = sum_of_lengths / len(column_values)
        return (sum_of_lengths > 50000) and (average_length > 20)

    @staticmethod
    def get_unique_values(db_path: str) -> Dict[str, Dict[str, List[str]]]:
        """
        Retrieves unique text values from the database excluding primary keys.

        Args:
            db_path (str): The path to the SQLite database file.

        Returns:
            Dict[str, Dict[str, List[str]]]: A dictionary containing unique values for each table and column.
        """
        cursor = SqliteDbUtils.get_cursor_from_path(db_path)

        table_names = SqliteDbUtils.get_all_table_names(cursor=cursor)

        primary_key_columns = SqliteDbUtils.get_all_primary_keys(cursor, table_names)
        primary_keys = []
        for column_names in primary_key_columns:
            for column_name in column_names:
                if column_name.lower() not in [c.lower() for c in primary_keys]:
                    primary_keys.append(column_name)

        unique_values: Dict[str, Dict[str, List[str]]] = {}
        for table_name in table_names:
            if table_name == "sqlite_sequence":
                continue
            logger.info(f"Processing {table_name}")
            text_columns = [col[1] for col in SqliteDbUtils.execute_sql(db_path,
                                                                        sql=SqliteDbUtils.get_sql_table_info(
                                                                            table_name),
                                                                        fetch="all") if
                            ("TEXT" in col[2] and col[1].lower() not in [c.lower() for c in primary_keys])]

            table_values: Dict[str, List[str]] = {}
            for column in text_columns:
                if any(keyword in column.lower() for keyword in
                       ["_id", " id", "url", "email", "web", "time", "phone", "date", "address"]) \
                        or column.endswith("Id") or column.endswith("id"):
                    continue

                result = SqliteDbUtils.execute_sql(db_path, f"""
                    SELECT SUM(LENGTH(unique_values)), COUNT(unique_values)
                    FROM (
                        SELECT DISTINCT `{column}` AS unique_values
                        FROM `{table_name}`
                        WHERE `{column}` IS NOT NULL
                    ) AS subquery
                """, fetch="one")

                sum_of_lengths, count_distinct = result
                if sum_of_lengths is None or count_distinct == 0:
                    continue

                average_length = sum_of_lengths / count_distinct
                logger.info(f"Column: {column}, sum_of_lengths: {sum_of_lengths}, "
                            f"count_distinct: {count_distinct}, average_length: {average_length}")

                if ("name" in column.lower() and sum_of_lengths < 5000000) \
                        or (sum_of_lengths < 2000000 and average_length < 25):
                    logger.info(f"Fetching distinct values for {column}")
                    sql = SqliteDbUtils.SQL_GET_COLUMN_NOT_NULL_DISTINCT.format(table_name=table_name,
                                                                                column_name=column)
                    values = [str(value[0]) for value in SqliteDbUtils.execute_sql(db_path,
                                                                                   sql=sql,
                                                                                   fetch="all")]
                    logger.info(f"Number of different values: {len(values)}")
                    table_values[column] = values

            unique_values[table_name] = table_values

        return unique_values

    @staticmethod
    def check_value_exists(db_path: str, table_name: str, column_name: str, value: str) -> Optional[str]:
        """
        Checks if a value exists in a column of a table in the database.

        Args:
            db_path (str): Path to the database file.
            table_name (str): The name of the table.
            column_name (str): The name of the column.
            value (str): The value to check.

        Returns:
            Optional[str]: The value if it exists, otherwise None.
        """
        query = f"SELECT {column_name} FROM {table_name} WHERE {column_name} LIKE '%{value}%' LIMIT 1"
        result = SqliteDbUtils.execute_sql(db_path, query, "one")
        return result[0] if result else None

    @staticmethod
    def aggregate_columns(columns_dicts: List[Dict[str, Any]], selected_tables: List[str],
                          merge_cot=True, question_id=None) -> Dict[str, List[str]]:
        """
        Aggregates columns from multiple responses and consolidates reasoning.

        Args:
            columns_dicts (List[Dict[str, Any]]): List of dictionaries containing column names and reasoning.
            selected_tables (List[str]): List of selected tables.

        Returns:
            Dict[str, List[str]]: Aggregated result with unique column names and consolidated reasoning.
        """
        question_id_msg = "" if question_id is None else f", question_id: {question_id}"
        # logger.info(f"Aggregating columns from multiple responses{question_id_msg}")
        columns = {}
        chain_of_thoughts = []
        for column_dict in columns_dicts:
            valid_column_dict = False
            dict_cot = None
            for key, value in column_dict.items():
                if key == "chain_of_thought_reasoning":
                    dict_cot = value
                else:  # key is table name
                    table_name = key
                    if table_name.startswith("`"):
                        table_name = table_name[1:-1]
                    column_names = value
                    if table_name.lower() in [t.lower() for t in selected_tables]:
                        for column_name in column_names:
                            if column_name.startswith("`"):
                                column_name = column_name[1:-1]
                            if table_name not in columns:
                                columns[table_name] = []
                            if column_name.lower() not in [col.lower() for col in columns[table_name]]:
                                columns[table_name].append(column_name)
                            valid_column_dict = True
            if valid_column_dict and dict_cot:
                chain_of_thoughts.append(dict_cot)

        # logger.info(f"Aggregated columns: {columns}")
        return columns

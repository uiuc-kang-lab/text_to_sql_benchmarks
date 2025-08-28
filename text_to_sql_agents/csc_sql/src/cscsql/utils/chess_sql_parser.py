from pathlib import Path
from typing import List, Optional, Dict

from sqlglot import parse_one, exp
from sqlglot.optimizer.qualify import qualify

from cscsql.utils.logger_utils import logger
from cscsql.utils.sqlite_db_utils import SqliteDbUtils
from cscsql.utils.string_utils import StringUtils

__all__ = [
    "ChessSchemaParser"
]


class ChessSchemaParser(object):

    @staticmethod
    def get_sql_tables(db_path: str, sql: str, clean_chess: bool = True) -> List[str]:
        """
        Retrieves table names involved in an SQL query.

        Args:
            db_path (str): Path to the database file.
            sql (str): The SQL query string.
            clean_chess:

        Returns:
            List[str]: List of table names involved in the SQL query.
        """
        cursor = SqliteDbUtils.get_cursor_from_path(db_path)

        db_tables = SqliteDbUtils.get_all_table_names(cursor, clean_chess=clean_chess)
        try:
            parsed_tables = list(parse_one(sql, read='sqlite').find_all(exp.Table))
            correct_tables = [
                StringUtils.clean_chess_str(str(table.name).strip())
                for table in parsed_tables
                if str(table.name).strip().lower() in [db_table.lower() for db_table in db_tables]
            ]
            return correct_tables
        except Exception as e:
            logger.warn(f"Error in get_sql_tables: {e}\nSQL: {sql}")
            raise e

    @staticmethod
    def _get_main_parent(expression: exp.Expression) -> Optional[exp.Expression]:
        """
        Retrieves the main parent expression for a given SQL expression.

        Args:
            expression (exp.Expression): The SQL expression.

        Returns:
            Optional[exp.Expression]: The main parent expression or None if not found.
        """
        parent = expression.parent
        while parent and not isinstance(parent, exp.Subquery):
            parent = parent.parent
        return parent

    @staticmethod
    def _get_table_with_alias(parsed_sql: exp.Expression, alias: str) -> Optional[exp.Table]:
        """
        Retrieves the table associated with a given alias.

        Args:
            parsed_sql (exp.Expression): The parsed SQL expression.
            alias (str): The table alias.

        Returns:
            Optional[exp.Table]: The table associated with the alias or None if not found.
        """
        return next((table for table in parsed_sql.find_all(exp.Table) if table.alias == alias), None)

    @staticmethod
    def get_sql_columns_dict(db_path: str, sql: str, clean_chess=True) -> Dict[str, List[str]]:
        """
        Retrieves a dictionary of tables and their respective columns involved in an SQL query.

        Args:
            db_path (str): Path to the database file.
            sql (str): The SQL query string.
            clean_chess (str): The SQL query string.

        Returns:
            Dict[str, List[str]]: Dictionary of tables and their columns.
        """
        columns_dict = {}

        try:
            if isinstance(db_path, str) or isinstance(db_path, Path):
                cursor = SqliteDbUtils.get_cursor_from_path(db_path)
            else:
                cursor = db_path

            sql = qualify(parse_one(sql, read='sqlite'), qualify_columns=True,
                          validate_qualify_columns=False) if isinstance(sql, str) else sql

            sub_queries = [subq for subq in sql.find_all(exp.Subquery) if subq != sql]
            for sub_query in sub_queries:
                subq_columns_dict = ChessSchemaParser.get_sql_columns_dict(cursor, sub_query)
                for table, columns in subq_columns_dict.items():
                    if table not in columns_dict:
                        columns_dict[table] = columns
                    else:
                        columns_dict[table].extend(
                            [col for col in columns if col.lower() not in
                             [c.lower() for c in columns_dict[table]]])

            for column in sql.find_all(exp.Column):
                column_name = column.name
                table_alias = column.table
                table = ChessSchemaParser._get_table_with_alias(sql, table_alias) if table_alias else None
                table_name = table.name if table else None

                if not table_name:
                    candidate_tables = [t for t in sql.find_all(exp.Table) if
                                        ChessSchemaParser._get_main_parent(t) == ChessSchemaParser._get_main_parent(
                                            column)]
                    for candidate_table in candidate_tables:
                        table_columns = SqliteDbUtils.get_table_column_names(cursor,
                                                                             candidate_table.name,
                                                                             clean_chess=clean_chess)
                        if column_name.lower() in [col.lower() for col in table_columns]:
                            table_name = candidate_table.name
                            break

                if table_name:
                    if table_name not in columns_dict:
                        columns_dict[table_name] = []
                    if column_name.lower() not in [c.lower() for c in columns_dict[table_name]]:
                        columns_dict[table_name].append(column_name)
        except Exception as e:
            # traceback.print_exc()
            logger.warning(f"parse sql column error: sql:{sql} - {e}")
            pass

        return columns_dict

import os
import sqlite3

from functools import lru_cache
from typing import Any

from loguru import logger


def get_sqlite_database_file(base_dir: str, database: str) -> str:
    """get path to sqlite database file based on dataset and database name"""
    # support nested and flat directory structures
    sqlite_flat_path = os.path.join(base_dir, database + ".sqlite")
    sqlite_nested_path = os.path.join(base_dir, database, database + ".sqlite")
    for sqlite_path in [sqlite_flat_path, sqlite_nested_path]:
        if os.path.exists(sqlite_path):
            return sqlite_path
    raise FileNotFoundError(f"Database file for {database=} not found in {base_dir=}")


@lru_cache(maxsize=1024)
def query_sqlite_database(base_dir: str, database: str, sql_query: str) -> list[dict]:
    """query sqlite database and return results"""
    db_path = get_sqlite_database_file(base_dir=base_dir, database=database)
    uri = "file:" + db_path + "?mode=ro"
    connection = sqlite3.connect(uri, uri=True)
    connection.row_factory = sqlite3.Row
    cursor = connection.cursor()
    result = cursor.execute(sql_query)
    json_result = [dict(r) for r in result.fetchall()]
    connection.close()
    return json_result


@lru_cache(maxsize=1024)
def query_sqlite_database_from_connection(connection, sql_query: str) -> list[dict]:
    """query sqlite database and return results"""
    cursor = connection.cursor()
    result = cursor.execute(sql_query)
    json_result = [dict(r) for r in result.fetchall()]
    return json_result


def get_sqlite_schema(base_dir: str, database: str) -> dict[str, Any]:
    """get sqlite schema, columns, relations as a dictionary"""
    database_path = get_sqlite_database_file(base_dir=base_dir, database=database)
    connection = sqlite3.connect(database_path)
    cursor = connection.cursor()

    schema = {"tables": {}}

    # Get table names
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
    tables = cursor.fetchall()
    
    table_primary_keys = {}
    for table in tables:
        table_name = table[0]
        # Get primary key information
        cursor.execute(f"PRAGMA table_info('{table_name}')")
        columns = cursor.fetchall()
        for column in columns:
            cid, col_name, col_type, is_notnull, default_value, is_pk = column
            if is_pk:
                table_primary_keys[table_name] = col_name
                break

    for table in tables:
        if table[0] in ["sqlite_sequence", "sqlite_stat1", "sqlite_stat4"]:
            continue
        table_name = table[0]
        schema["tables"][table_name] = {"columns": {}, "keys": {}, "foreign_keys": {}}

        # Get column information
        cursor.execute(f"PRAGMA table_info('{table_name}')")
        columns = cursor.fetchall()
        for column in columns:
            cid, col_name, col_type, is_notnull, default_value, is_pk = column
            schema["tables"][table_name]["columns"][col_name] = col_type
            if is_pk:
                schema["tables"][table_name]["keys"]["primary_key"] = [col_name]

        # Get foreign key information
        cursor.execute(f"PRAGMA foreign_key_list('{table_name}')")
        foreign_keys = cursor.fetchall()
        for fk in foreign_keys:
            _, _, ref_table, col_name, ref_col, *_ = fk

            # If ref_col is None, use the primary key of the referenced table
            if ref_col is None or ref_col == "":
                ref_col = table_primary_keys.get(ref_table)
                
            schema["tables"][table_name]["foreign_keys"][col_name] = {
                "referenced_table": ref_table,
                "referenced_column": ref_col,
            }

    cursor.close()
    connection.close()
    return schema


def analyze_database(base_dir: str, database: str):
    """query sqlite database and return status and results"""
    db_path = get_sqlite_database_file(base_dir=base_dir, database=database)
    connection = sqlite3.connect(db_path)
    cursor = connection.cursor()

    cursor.execute("PRAGMA analysis_limit=10000;")
    cursor.execute("ANALYZE;")
    # This fixes the hanging queries, the fix comes from the main author of sqlite Richard Hipp himself
    # Only needed for some versions of sqlite somehow, I don't understand it much
    # https://sqlite.org/forum/info/aac5dfa3fc3fb68fdf3c291d15545b51bbea98939e814b1575aad884ef500e09 more here

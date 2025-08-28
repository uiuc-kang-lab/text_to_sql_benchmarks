import sqlite3
import threading
from enum import Enum
from typing import Optional, List, Tuple
from functools import lru_cache
from prettytable import PrettyTable
import sqlglot

class SQLExecutionResultType(Enum):
    """
    Type of the result of a SQL query execution.
    
    Attributes:
        SUCCESS: The query is executed successfully.
        TIMEOUT: The query execution timed out.
        ERROR: The query execution failed.
    """
    SUCCESS = "success"
    TIMEOUT = "timeout"
    ERROR = "error"
    
class SQLExecutionResult:
    """
    Result of a SQL query execution.
    """
    def __init__(self, db_path: str, sql: str, result_type: SQLExecutionResultType, result_cols: Optional[List[str]], result: Optional[List[Tuple]], error_message: Optional[str]) -> None:
        self.db_path = db_path
        self.sql = sql
        self.result_type = result_type
        self.result_cols = result_cols
        self.result = result
        self.error_message = error_message
        
    def to_dict(self) -> dict:
        return {
            "db_path": self.db_path,
            "sql": self.sql,
            "result_type": self.result_type.value,
            "result_cols": self.result_cols,
            "result": self.result,
            "error_message": self.error_message
        }

class ExecuteSQLThread(threading.Thread):
    """
    Thread to execute a SQL query.
    """
    def __init__(self, db_path: str, query: str, timeout: int) -> None:
        super().__init__()
        self.db_path = db_path
        self.query = query
        self.timeout = timeout
        self.result_cols = None
        self.result = None
        self.exception = None
        
        self.stop_event = threading.Event()
        
    def run(self) -> None:
        def check_stop():
            if self.stop_event.is_set():
                raise Exception("Query execution cancelled")
        
        try:
            # Enforce to read-only mode, to prevent accidental modification of the database
            with sqlite3.connect(f'file:{self.db_path}?mode=ro', uri=True) as conn:
                conn.text_factory = lambda x: str(x, 'utf-8', errors='replace')  # Add error handling for UTF-8 decoding
                conn.set_progress_handler(check_stop, 1000)
                cursor = conn.cursor()
                cursor.execute(self.query)
                self.result_cols = [col[0] for col in cursor.description]
                self.result = cursor.fetchall()
        except Exception as e:
            self.exception = e

def execute_sql_with_timeout(db_path: str, query: str, timeout: int = 60) -> SQLExecutionResult:
    """
    Execute a SQL query synchronously with a timeout.
    
    Args:
        db_path: The path to the database.
        query: The SQL query to execute.
        timeout: The timeout.
    Returns:
        The result of the SQL query.
    """ 
    thread = ExecuteSQLThread(db_path, query, timeout)
    thread.daemon = True
    thread.start()
    thread.join(timeout)
    if thread.is_alive():
        thread.stop_event.set()
        thread.join(1)
        error_message = f"SQL execution timed out after {timeout} seconds"
        return SQLExecutionResult(db_path, query, SQLExecutionResultType.TIMEOUT, None, None, error_message)
    if thread.exception:
        error_message = str(thread.exception)
        return SQLExecutionResult(db_path, query, SQLExecutionResultType.ERROR, None, None, error_message)
    return SQLExecutionResult(db_path, query, SQLExecutionResultType.SUCCESS, thread.result_cols, thread.result, None)

def execute_sql_without_timeout(db_path: str, query: str) -> SQLExecutionResult:
    """
    Execute a SQL query without a timeout.
    
    Args:
        db_path: The path to the database.
        query: The SQL query to execute.
    Returns:
        The result of the SQL query.
    """
    try:
        with sqlite3.connect(f'file:{db_path}?mode=ro', uri=True) as conn:
            conn.text_factory = lambda x: str(x, 'utf-8', errors='replace')  # Add error handling for UTF-8 decoding
            cursor = conn.cursor()
            cursor.execute(query)
            result_cols = [col[0] for col in cursor.description]
            result = cursor.fetchall()
            return SQLExecutionResult(db_path, query, SQLExecutionResultType.SUCCESS, result_cols, result, None)
    except Exception as e:
        return SQLExecutionResult(db_path, query, SQLExecutionResultType.ERROR, None, None, str(e))

# def normalize_sql(sql: str) -> str:
#     """
#     Normalize a SQL query.
    
#     Args:
#         sql: The SQL query to normalize.
#     Returns:
#         The normalized SQL query.
#     """
#     if sql.startswith("```sql") and sql.endswith("```"):
#         sql = sql[6:-3]
#     norm_sql = sql.replace(";", "").replace("\n", " ").replace("\t", " ").replace("\\n", " ")
#     while "  " in norm_sql:
#         norm_sql = norm_sql.replace("  ", " ")
#     return norm_sql.strip()

def normalize_sql(sql: str) -> str:
    """
    Normalize a SQL query.
    
    Args:
        sql: The SQL query to normalize.
    Returns:
        The normalized SQL query.
    """
    sql = sql.strip()
    if sql.startswith("```sql") and sql.endswith("```"):
        sql = sql[6:-3]
    try:
        parsed = sqlglot.parse_one(sql, dialect="sqlite")
        return parsed.sql(dialect="sqlite", normalize=True, pretty=False, comments=False)
    except Exception as e:
        return sql

@lru_cache(maxsize=10000)
def _cached_execute_sql_with_timeout(db_path: str, sql_query: str) -> SQLExecutionResult:
    result = execute_sql_with_timeout(db_path, sql_query)
    return result

def cached_execute_sql_with_timeout(db_path: str, sql_query: str) -> SQLExecutionResult:
    # sql_query = normalize_sql(sql_query)
    result = _cached_execute_sql_with_timeout(db_path, sql_query)
    return result

def is_valid_execution_result(result: SQLExecutionResult) -> bool:
    if result.result_type is not SQLExecutionResultType.SUCCESS:
        return False
    return any(any(col is not None for col in row) for row in result.result)
    # return True

def format_execution_result(result: SQLExecutionResult, row_limit: int = 3, val_length_limit: int = 100) -> str:
    if result.result_type == SQLExecutionResultType.SUCCESS:
        table = PrettyTable()
        # if the result_cols has non-unique values, add a suffix to the column name
        # since table.field_names cannot have duplicate values
        if len(result.result_cols) != len(set(result.result_cols)):
            result.result_cols = [col + "_" + str(i) for i, col in enumerate(result.result_cols)]
        table.field_names = result.result_cols
        truncated_result = []
        for row in result.result[:row_limit]:
            truncated_row = []
            for i, val in enumerate(row):
                if isinstance(val, str) and len(val) > val_length_limit:
                    truncated_row.append(val[:val_length_limit] + "...")
                else:
                    truncated_row.append(val)
            truncated_result.append(truncated_row)
        table.add_rows(truncated_result)
        return str(table)
    else:
        return result.error_message

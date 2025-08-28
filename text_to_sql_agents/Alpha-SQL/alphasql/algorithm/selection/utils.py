from sqlglot import parse_one, exp
from collections import defaultdict
from typing import Dict, List, Set
from alphasql.database.schema import TableSchema
from alphasql.database.sql_execution import execute_sql_with_timeout, SQLExecutionResultType
import copy
import time
import numpy as np

def extract_tables_and_columns(query: str, dialect="sqlite", lower=True):
    ast = parse_one(query, dialect=dialect)
    table_names = ast.find_all(exp.Table)
    column_names = ast.find_all(exp.Column)
    return {
        "table_names": list(set([_table.name if not lower else _table.name.lower() for _table in table_names])),
        "column_names": list(set([_column.name if not lower else _column.name.lower() for _column in column_names]))
    }
    
def union_tables_and_columns(tables_and_columns_1: Dict[str, List[str]], tables_and_columns_2: Dict[str, List[str]]):
    return {
        "table_names": list(set(tables_and_columns_1["table_names"] + tables_and_columns_2["table_names"])),
        "column_names": list(set(tables_and_columns_1["column_names"] + tables_and_columns_2["column_names"]))
    }
    
def tables_and_columns_to_schema_selection_dict(tables_and_columns: Dict[str, List[str]], table_schema_dict: Dict[str, "TableSchema"]):
    schema_selection_dict = {}
    for table_name, table_schema in table_schema_dict.items():
        if table_name.lower() in tables_and_columns["table_names"]:
            schema_selection_dict[table_name] = []
            for column_name in table_schema.columns.keys():
                if column_name.lower() in tables_and_columns["column_names"]:
                    schema_selection_dict[table_name].append(column_name)
    return schema_selection_dict

def measure_sql_execution_time(db_path: str, sql_query: str, repeat: int = 10) -> float:
    execution_times = []
    for _ in range(repeat):
        start_time = time.time()
        execution_result = execute_sql_with_timeout(db_path, sql_query)
        if execution_result.result_type == SQLExecutionResultType.SUCCESS:
            end_time = time.time()
            execution_times.append(end_time - start_time)
    # remove outliers
    execution_time_std = np.std(execution_times)
    execution_time_mean = np.mean(execution_times)
    execution_times = [execution_time for execution_time in execution_times if execution_time > execution_time_mean - 3 * execution_time_std and execution_time < execution_time_mean + 3 * execution_time_std]
    return np.mean(execution_times)
    
def get_subset_schema_dict(table_schema_dict: Dict[str, "TableSchema"], schema_selection_dict: Dict[str, List[str]]):
    selected_table_names_lower = [selected_table_name.lower() for selected_table_name in schema_selection_dict.keys()]
    new_table_schema_dict = {}
    for selected_table_name, selected_column_names in schema_selection_dict.items():
        for original_table_name, original_table_schema in table_schema_dict.items():
            if selected_table_name.lower() == original_table_name.lower():
                new_table_schema = TableSchema(table_name=original_table_name, columns={})
                for original_column_name, original_column_schema in original_table_schema.columns.items():
                    is_selected = False
                    for selected_column_name in selected_column_names:
                        if selected_column_name.lower() == original_column_name.lower():
                            is_selected = True
                            break
                    if original_column_schema.primary_key:
                        # if the column is a primary key, it must be selected
                        is_selected = True
                    for target_table_name, target_column_name in original_column_schema.foreign_keys:
                        if target_table_name.lower() in selected_table_names_lower:
                            # if the column is a foreign key and the target table is selected, it must be selected
                            is_selected = True
                            break
                    for source_table_name, source_column_name in original_column_schema.referenced_by:
                        if source_table_name.lower() in selected_table_names_lower:
                            # if the column is a referenced by and the source table is selected, it must be selected
                            is_selected = True
                            break
                    if is_selected:
                        new_column_schema = copy.deepcopy(original_column_schema)
                        _foreign_keys = []
                        _referenced_by = []
                        for target_table_name, target_column_name in original_column_schema.foreign_keys:
                            if target_table_name.lower() in selected_table_names_lower:
                                _foreign_keys.append((target_table_name, target_column_name))
                        for source_table_name, source_column_name in original_column_schema.referenced_by:
                            if source_table_name.lower() in selected_table_names_lower:
                                _referenced_by.append((source_table_name, source_column_name))
                        new_column_schema.foreign_keys = _foreign_keys
                        new_column_schema.referenced_by = _referenced_by
                        new_table_schema.columns[original_column_name] = new_column_schema
                new_table_schema_dict[original_table_name] = new_table_schema
    return new_table_schema_dict

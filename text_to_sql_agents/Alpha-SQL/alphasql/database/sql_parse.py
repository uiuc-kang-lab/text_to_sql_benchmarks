from sqlglot import parse_one, exp
from sqlglot.optimizer.qualify import qualify
from sqlglot.optimizer.scope import build_scope
from typing import List, Dict, Tuple, Any
from collections import defaultdict
from alphasql.database.schema import DatabaseSchema
from alphasql.database.database_manager import DatabaseManager

def get_schema_dict_for_sqlglot(database_schema: DatabaseSchema):
    schema = defaultdict(dict)
    for table_name, table_schema in database_schema.tables.items():
        for column_name, column_schema in table_schema.columns.items():
            schema[table_name][column_name] = column_schema.column_type
    return schema

def extract_db_values_from_sql(sql: str, dialect: str = "sqlite", database_schema: DatabaseSchema = None) -> Dict[Tuple[str, str], List[str]]:
    """
    Extract the database values from a SQL query.
    
    Args:
        sql (str): The SQL query.
        dialect (str): The dialect of the SQL query.
        database_schema (DatabaseSchema): The database schema.
    
    Returns:
        A dictionary with tuple of (table name, column name) as key, and a list of relevant values as value.
    """
    parsed_sql = parse_one(sql, dialect=dialect)
    db_values = defaultdict(list)
    schema = get_schema_dict_for_sqlglot(database_schema) if database_schema else None
    try:
        qualified_sql = qualify(parsed_sql, schema=schema)
    except Exception as e:
        qualified_sql = parsed_sql
    
    # get table alias mapping
    root = build_scope(qualified_sql)
    schema = {table.lower(): {column_name.lower(): column_type for column_name, column_type in columns.items()}
            for table, columns in schema.items()}
    
    table_alias_mapping = defaultdict(list)
    for scope in root.traverse():
        for alias, (node, source) in scope.selected_sources.items():
            if isinstance(source, exp.Table):
                # same alias in multiple queries
                table_alias_mapping[alias].append(str(source.this).replace("\"", ""))
    
    for condition_expr in qualified_sql.find_all(exp.EQ):
        if isinstance(condition_expr.this, exp.Column) and isinstance(condition_expr.expression, exp.Literal):
            # double check if the column is in the database schema
            parsed_table_name = condition_expr.this.table
            parsed_column_name = condition_expr.this.name
            actual_table_name = None
            actual_column_name = None
            
            if parsed_table_name in table_alias_mapping.keys():
                for table_name in table_alias_mapping[parsed_table_name]:
                    all_table_columns = [col.lower() for col in schema[table_name].keys()]
                    if parsed_column_name.lower() in all_table_columns:
                        parsed_table_name = table_name
            
            is_parsed_column_actual = False
            for table_name, table_schema in database_schema.tables.items():
                if table_name.lower() == parsed_table_name.lower():
                    actual_column_names = [column_name for column_name in table_schema.columns.keys()]
                    parsed_column_name_idx = -1
                    for i, actual_column_name in enumerate(actual_column_names):
                        if parsed_column_name.lower() == actual_column_name.lower():
                            parsed_column_name_idx = i
                            break
                    if parsed_column_name_idx != -1:
                        is_parsed_column_actual = True
                        actual_table_name = table_name
                        actual_column_name = actual_column_names[parsed_column_name_idx]
                        break
            if is_parsed_column_actual:
                db_values[(actual_table_name, actual_column_name)].append(condition_expr.expression.name)
    return db_values

if __name__ == "__main__":
    database_schema = DatabaseManager.get_database_schema("card_games", "data/bird/dev/dev_databases")
    print(extract_db_values_from_sql(
        "SELECT COUNT(id) FROM cards WHERE setCode IN ( SELECT code FROM sets WHERE name = 'World Championship Decks 2004' ) AND convertedManaCost = 3", 
        database_schema=database_schema
    ))
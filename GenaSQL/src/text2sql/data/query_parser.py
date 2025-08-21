# get mapping of db tables to columns
# use sql_metadata and sqlglot due to edge-case issues with both

from collections import defaultdict

import sqlglot
from sql_metadata import Parser


# sqlglot functions
def schema_info_to_column_table_map(schema_info: dict) -> dict:
    """convert 'schema info' dict into 'inverted' column -> tables dict"""
    col_map = defaultdict(list)
    for table_name, table_data in schema_info["tables"].items():
        for col in table_data["columns"]:
            col_map[col].append(table_name)
    return col_map


def sqlglot_extract_column_names(sql: str) -> list[str]:
    parsed = sqlglot.parse_one(sql, dialect="sqlite")
    columns = parsed.find_all(sqlglot.expressions.Column)
    column_info = set()
    for col in columns:
        if col.table:
            column_info.add(f"{col.table}.{col.name}")
        else:
            column_info.add(col.name)

    return list(column_info)


def sqlglot_extract_table_names(sql: str) -> list[str]:
    parsed = sqlglot.parse_one(sql, dialect="sqlite")
    tables = parsed.find_all(sqlglot.expressions.Table)
    return [t.name for t in tables]


def sqlglot_extract_projections(sql: str) -> list[str]:
    parsed = sqlglot.parse_one(sql, dialect="sqlite")
    selects = parsed.find_all(sqlglot.expressions.Select)
    projection_info = set()
    for select in selects:
        for projection in select.expressions:
            projection_info.add(projection.alias_or_name)
    return list(projection_info)


def sqlmeta_extract_column_names(sql: str) -> list[str]:
    parser = Parser(sql)
    return list(parser.columns)


def sqlmeta_extract_table_names(sql: str) -> list[str]:
    parser = Parser(sql)
    return list(parser.tables)


def sqlmeta_extract_table_aliases(sql: str) -> dict:
    parser = Parser(sql)
    return dict(parser.tables_aliases)


def parse_sql(sql: str) -> dict:
    """parse sql query and get tables, columns, etc."""
    try:
        sqlg_cols = sqlglot_extract_column_names(sql)
    except sqlglot.errors.ParseError:
        sqlg_cols = []

    try:
        sqlg_tables = sqlglot_extract_table_names(sql)
    except sqlglot.errors.ParseError:
        sqlg_tables = []

    try:
        projections = sqlglot_extract_projections(sql)
    except sqlglot.errors.ParseError:
        projections = []

    try:
        sqlm_cols = sqlmeta_extract_column_names(sql)
    except Exception as e:
        sqlm_cols = []

    try:
        sqlm_tables = sqlmeta_extract_table_names(sql)
    except Exception as e:
        sqlm_tables = []

    try:
        aliases = sqlmeta_extract_table_aliases(sql)
    except Exception as e:
        aliases = dict()

    # combine
    tables = [t for t in list(set(sqlg_tables + sqlm_tables)) if "*" not in t]
    columns = list(set(sqlg_cols + sqlm_cols))
    # sort so that columns with '.' come first
    columns = sorted(columns, key=lambda x: x.count("."), reverse=True)
    projections = [p for p in projections if "*" not in p]

    return {
        "tables": tables,
        "columns": columns,
        "projections": projections,
        "aliases": aliases,
    }


def get_table_mapping(schema_info: dict, sql: str) -> dict:
    """based on the schema info dict and query, get mapping of tables to columns"""
    # get map of column -> tables from the
    col_map = schema_info_to_column_table_map(schema_info)
    col_map = {k.lower(): (v, k) for k, v in col_map.items()}
    # pprint("col_map")
    # pprint(col_map)
    # parse sql with both methods and combine results
    results = parse_sql(sql)
    tables = results["tables"]
    columns = results["columns"]
    projections = results["projections"]
    aliases = results["aliases"]
    aliases = {k.lower(): v for k, v in aliases.items()}

    # final result is dict with key = table, value = list of mentioned columns
    table_set_map = defaultdict(set)
    for column in columns:
        # remove quotations
        column = column.replace("`", "").replace('"', "").replace("'", "")
        # for columns parsed as table.column, check table exists
        if "." in column:
            tbl, col = column.split(".")
            if tbl in tables:
                table_set_map[tbl].add(col)
            elif tbl.lower() in aliases:
                table_set_map[aliases[tbl.lower()]].add(col)
        # otherwise, check if column exists in any table
        else:
            all_col_tables, column_correct = col_map.get(column.lower(), ([], None))
            # add for all sql expression tables
            for tbl in all_col_tables:
                tables_lower = [table.lower() for table in tables]
                if tbl.lower() in tables_lower:
                    table_set_map[tbl].add(column_correct)
    table_map = dict()
    for tbl, cols in table_set_map.items():
        table_map[tbl] = list(cols)

    return {
        "tables": tables,
        "columns": columns,
        "projections": projections,
        "aliases": aliases,
        "table_map": table_map,
    }

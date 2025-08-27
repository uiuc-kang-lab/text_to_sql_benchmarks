import json
import re

import sqlparse

from sql_metadata import Parser


def get_table_names_from_query(query: str) -> list[str]:
    """try to extract mentioned tables from SQL query"""
    try:
        predicted_tables: list[str] = list(Parser(query).tables)
    except Exception as e:
        predicted_tables = []
    return predicted_tables


def normalize_sql(query):
    """
    Normalize SQL query by removing extra spaces and formatting consistently.
    """
    return sqlparse.format(query, reindent=True, keyword_case="upper")


def extract_sql_query(text):
    """
    Extracts SQL query from a string containing comments and query.
    Removes comments (lines starting with --) and empty lines.

    Args:
        text (str): Input text containing SQL query and comments

    Returns:
        str: Clean SQL query without comments
    """
    # Split the text into lines
    lines = text.strip().split("\n")

    # Filter out comments and empty lines
    sql_lines = []
    for line in lines:
        line = line.strip()
        # Skip empty lines and comment lines
        if not line or line.startswith("--"):
            continue
        sql_lines.append(line)

    # Join the remaining lines back together
    return "\n".join(sql_lines)


def extract_last_json_block(text: str) -> str:
    """extract code block contents"""
    pattern = r"```(?:json|sql|python|\w*)\n?(.*?)\n?```"
    matches = re.finditer(pattern, text, re.DOTALL)
    results = []
    for match in matches:
        content = match.group(1).strip()
        results.append(content)
    if len(results) == 0:
        return text
    return results[-1]


def parse_json_from_prediction(prediction: str) -> dict:
    """extract json prediction from"""
    json_body = extract_last_json_block(prediction)
    json_data = json.loads(json_body)
    return json_data

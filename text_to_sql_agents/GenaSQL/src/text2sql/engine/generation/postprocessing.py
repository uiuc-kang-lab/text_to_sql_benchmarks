import re
import json

def extract_first_code_block(text: str) -> str:
    """extract code block contents"""
    pattern = r'```(?:sql|python|\w*)\n?(.*?)\n?```'
    matches = re.finditer(pattern, text, re.DOTALL)
    results = []
    for match in matches:
        content = match.group(1).strip()
        results.append(content)
    if len(results) == 0:
        return None
    return results[0]


def extract_sql_from_json(text: str) -> str:
    text = text.replace("```json", "").replace("```", "")
    text = json.loads(text)
    return text.get("sql", text.get("SQL"))

import re


def check_table_alias(sql, table_name):

    sql_keywords = [
        'ON', 'LEFT JOIN', 'RIGHT JOIN', 'INNER JOIN', 'OUTER JOIN',
        'JOIN', 'WHERE', 'GROUP', 'ORDER', 'LIMIT', r'\)'
    ]
    # Regular expression: match anywhere in SQL, find table names and their aliases
    # Matching rules: table name can be followed by AS and alias, or directly followed by alias
    pattern1 = r'["\b]?' + re.escape(table_name) + r'["\b]?(?:\s+AS\s+"?(\w+)"?|\s+"?(\w+)"?)?'

    # Search Matching Sections
    matches = re.findall(pattern1, sql, re.IGNORECASE)

    table_alias_mapping = []  # Used to hold the mapping of table names and aliases
    # If a non-null alias part of the result is matched, the alias was used.
    for match in matches:
        if match[0]:
            table_alias_mapping.append(match[0])
            #continue
        elif match[1] and not any(match[1].lower() in keyword.lower().split() for keyword in sql_keywords):
            table_alias_mapping.append(match[1])

    return table_alias_mapping, bool(table_alias_mapping)


def extract_select_statements(sql):
    # Regular expression matches SELECT clause, non-greedy pattern, matches to the end of the next ;or) that is not nested
    select_pattern = re.compile(r'(SELECT\b.*?)(?=SELECT\b|$)', re.IGNORECASE | re.DOTALL)

    # Find all SELECT statements
    select_statements = select_pattern.findall(sql)
    return [stmt.strip() for stmt in select_statements]

def extract_where_clause(sql):
    # Regular expression matches WHERE and what follows until the end of the GROUP BY, ORDER BY, or statement
    where_pattern = re.compile(r'(\bWHERE\b.*?)(?=\bGROUP BY\b|\bORDER BY\b|;|$)', re.IGNORECASE | re.DOTALL)

    # Search and extract WHERE clauses
    match = where_pattern.search(sql)
    if match:
        return match.group(1).strip()  # Returns the complete clause containing the WHERE
    else:
        return "No WHERE clause found"


def check_table_in_sql(sql, table_name):
    table_name = table_name.strip('"')
    # Match the exact table name to ensure that similar table names are not mistakenly matched
    pattern = re.compile(r'["`\[]' + re.escape(table_name) + r'.*?["`\]]|' + re.escape(table_name) + r'\S*', re.IGNORECASE)
    # pattern = re.compile(r'\`' + re.escape(table_name) + r'.*?\`|' + re.escape(table_name) + r'\S*', re.IGNORECASE)
    #pattern = re.compile(r'["`\[]?\b' + re.escape(table_name) + r'\b["`\[]?', re.IGNORECASE)
    find_list = re.findall(pattern, sql)
    return find_list


def check_column_in_where_clause(where_clause, column_name):
    real_condition_clause = ""
    value_flag = False
    column_name = column_name.strip('"')
    # A regular expression matches a condition like `a.column = b.column`.
    column_eq_pattern = re.compile(r'(\b\w*[A-Za-z]\w*\.)["`\[\b]?' + re.escape(column_name) + r'["`\]\b]?\s*=\s*(\b\w*[A-Za-z]\w*\.)(?:["`\[]\w+(?:\s*\w+)*["`\[]|\b\w+\b)', re.IGNORECASE)

    # Search on where clause to match special conditions (false conditions)
    match = list(column_eq_pattern.finditer(where_clause))

    if match:
        removeSpecial_clause = re.sub(column_eq_pattern, '', where_clause).strip()
        real_condition_clause = removeSpecial_clause    # Remove the where part of the statement after the special condition.
        condition_check_pattern = re.compile(r'(?:["\`\[])(' + re.escape(column_name) + r'.*?)(?:["\`\]])|(' + re.escape(column_name) + r')\b\S*', re.IGNORECASE)
        probably_match_table_list = condition_check_pattern.findall(removeSpecial_clause)
        probably_match_table_list = list({value.strip() for item in probably_match_table_list for value in item if value.strip()})
        if column_name.lower() in [item.lower() for item in probably_match_table_list]:
            condition_exist_flag = True
        else:
            condition_exist_flag = False
    else:
        condition_check_pattern = re.compile(r'(?:["\`\[])(' + re.escape(column_name) + r'.*?)(?:["\`\]])|(' + re.escape(column_name) + r')\b\S*', re.IGNORECASE)
        real_condition_clause = where_clause  # Without special conditions, the original where part of the statement is used directly
        probably_match_table_list = condition_check_pattern.findall(real_condition_clause)
        probably_match_table_list = list({value.strip() for item in probably_match_table_list for value in item if value.strip()})
        if column_name.lower() in [item.lower() for item in probably_match_table_list]:
            condition_exist_flag = True
        else:
            condition_exist_flag = False

    return condition_exist_flag, real_condition_clause

def value_condition_check(sql, column_name, table_name):
    # 1 Determine if the table is aliased in sql
    table_alias_all_mapping, use_alias_flag = check_table_alias(sql, table_name)  # table_alias_mapping holds the alias for the current table, which may be empty.
    # 2 Extract all SELECT clauses in SQL
    select_subClause_list = extract_select_statements(sql)
    # 3 For each SELECT clause extract pure WHERE clauses (WHERE clauses that exclude Group BY, ORDER BY parts)
    for idx, select_subClause in enumerate(select_subClause_list):
        table_alias_subClause_mapping, use_alias_flag = check_table_alias(select_subClause, table_name)  # table_alias_mapping holds the alias for the current table, which may be empty.
        where_clause = extract_where_clause(select_subClause)
        condition_exist_flag, real_condition_clause = check_column_in_where_clause(where_clause, column_name)
        if condition_exist_flag:
            # re.compile(r'["`\[]' + re.escape(table_name) + r'.*?["`\]]|' + re.escape(table_name) + r'\S*',re.IGNORECASE)
            column_extract_pattern = re.compile(r'(\b\w*[A-Za-z]\w*)\.(?:["`\[])(' + re.escape(column_name) + r'.*?)(?:["`\]])|(\b\w*[A-Za-z]\w*)\.(' + re.escape(column_name) + r')\b\S*', re.IGNORECASE)
            table_name_pattern_list = column_extract_pattern.findall(real_condition_clause)
            probably_table_name_list = []
            for item in table_name_pattern_list:
                if item[1].lower() == column_name.lower():
                    probably_table_name_list.append(item[0])
                elif item[3].lower() == column_name.lower():
                    probably_table_name_list.append(item[2])
            probably_table_name_list = list(set(probably_table_name_list))
            if set(table_alias_all_mapping) & set(probably_table_name_list):
                return True
            elif table_name in probably_table_name_list:
                return True
            elif table_name in select_subClause and not table_alias_subClause_mapping:
                removePointCondition_clause = re.sub(column_extract_pattern, '', real_condition_clause).strip()
                condition_check_pattern = re.compile(r'(?:["\`\[])(' + re.escape(column_name) + r'.*?)(?:["\`\]])|(' + re.escape(column_name) + r')\b\S*', re.IGNORECASE)
                removePointCondition_clause_match_table_list = condition_check_pattern.findall(removePointCondition_clause)
                removePointCondition_clause_match_table_list = list({value.strip() for item in removePointCondition_clause_match_table_list for value in item if value.strip()})
                if column_name.lower() in [item.lower() for item in removePointCondition_clause_match_table_list]:
                    return True
            else:
                continue
        else:
            # The column column_name does not have a value in the where section of the current select query block.
            continue

    return False

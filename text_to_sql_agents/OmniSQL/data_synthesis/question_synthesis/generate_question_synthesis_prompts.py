import json
import os
import random
import sqlite3
import numpy as np
import re
from tqdm import tqdm

style2desc = {
"Formal": '''**Formal Style**
   - Uses standard grammar and vocabulary.
   - Example: Find all students older than 18 years and return their home addresses.''',

"Colloquial": '''**Colloquial Style**
   - Employs informal vocabulary and expressions.
   - Example: Hey! Could you help me find all the students who are over 18? I'd love to know their names and where they live.''',

"Imperative": '''**Imperative Style**
   - Uses command or directive sentences.
   - Example: Could you please gather all the students who are older than 18? I really need to know their names and where they live!''',

"Interrogative": '''**Interrogative Style**
   - Uses question forms.
   - Example: Could you tell me which students are older than 18 and what their home addresses are?''',

"Descriptive": '''**Descriptive Style**
   - Uses detailed descriptions with contextual information.
   - Example: I want to know the names and home addresses of all students older than 18.''',

"Concise": '''**Concise Style**
   - Use short sentences.
   - Example: Students older than 18, return their names and addresses.''',

"Vague": '''**Vague Style**
   - Includes ambiguous vocabulary requiring inference.
   - Example: What are the names and addresses of those older students? (External Knowledge: 'older students' refers to age >= 18.)''',

"Metaphorical": '''**Metaphorical Style**
   - Uses metaphors or metaphorical expressions.
   - Example: Find the names and addresses of those who have reached adulthood. (External Knowledge: 'reached adulthood' refers to age >= 18.)''',

"Multi-turn Dialogue": '''**Multi-turn Dialogue Style**
    - This involves a dialogue to clarify the user's query needs.
    - Example: [{"User": "I want to query some student information."}, {"Assistant": "Which students' information would you like to query?"}, {"User": "Students older than 18."}, {"Assistant": "What other information would you like to know about them?"}, {"User": "Names and addresses."}, {"Assistant": "Is there anything else you need?"}, {"User": "No."}, {"Assistant": "OK, I will help you translate your request into an SQL query."}]'''
}

steps_wo_ek = '''1. **Explain the SQL Query:** Provide a detailed explanation of what the query does.
2. **Generate a Question:** Formulate a natural language question based on the SQL query and explanation.'''

steps_w_ek = '''1. **Explain the SQL Query:** Provide a detailed explanation of what the query does.
2. **Generate a Question:** Formulate a natural language question based on the SQL query and explanation.
3. **External Knowledge:** For Vague or Metaphorical styles, include external knowledge to enhance clarity.'''

steps_multi_round = '''1. **Explain the SQL Query:** Provide a detailed explanation of what the query does.
2. **Generate a Dialogue:** Create a conversation between the User and the Assistant based on the SQL query and its explanation.'''

guidelines_wo_ek = '''1. Clearly describe the columns being selected by the SQL query. For example:
   - "SELECT * ... FROM ..." means "Find all ...";
   - "SELECT f.check_date, f.status, f.remarks, c.year, c.year_min, c.year_max, c.year_average, c.data_quality_score FROM ..." means "Return the check dates, statuses, remarks, years, minimum years, maximum years, average years, and quality scores for ...".
2. Ensure the natural language question accurately captures the semantics of the SQL query, including conditions such as predicates, `ORDER BY`, and `LIMIT` clauses.'''

guidelines_w_ek = '''1. Clearly describe the columns being selected by the SQL query. For example:
   - "SELECT * ... FROM ..." means "Find all ...";
   - "SELECT f.check_date, f.status, f.remarks, c.year, c.year_min, c.year_max, c.year_average, c.data_quality_score FROM ..." means "Return the check dates, statuses, remarks, years, minimum years, maximum years, average years, and quality scores for ...".
2. Ensure the natural language question accurately captures the semantics of the SQL query, including conditions such as predicates, `ORDER BY`, and `LIMIT` clauses.
3. If necessary, incorporate external knowledge using multiple entries separated by semicolons (";"). These can include formulas, common sense, domain-specific knowledge, or extended context, such as information from long documents. Each entry should be concise.'''

guidelines_multi_round = '''1. Clearly describe the columns being selected by the SQL query. For example:
   - "SELECT * ... FROM ..." means "Find all ...";
   - "SELECT f.check_date, f.status, f.remarks, c.year, c.year_min, c.year_max, c.year_average, c.data_quality_score FROM ..." means "Return the check dates, statuses, remarks, years, minimum years, maximum years, average years, and quality scores for ...".
2. Ensure the conversation accurately captures the semantics of the SQL query, including conditions such as predicates, `ORDER BY`, and `LIMIT` clauses.'''

output_format_wo_ek = '''Please structure your response as follows:

[EXPLANATION-START]
(SQL Explanation)
[EXPLANATION-END]

[QUESTION-START]
(Natural Language Question)
[QUESTION-END]

- **SQL Explanation**: Provide a clear and detailed explanation of the SQL query, enclosed within [EXPLANATION-START] and [EXPLANATION-END].
- **Natural Language Question**: Translate the SQL query into a natural language question, enclosed within [QUESTION-START] and [QUESTION-END].'''

output_format_w_ek = '''Please structure your response as follows:

[EXPLANATION-START]
(SQL Explanation)
[EXPLANATION-END]

[QUESTION-START]
(Natural Language Question)
[QUESTION-END]

[EXTERNAL-KNOWLEDGE-START]
(External Knowledge)
[EXTERNAL-KNOWLEDGE-END]

- **SQL Explanation**: Provide a clear and detailed explanation of the SQL query, enclosed within [EXPLANATION-START] and [EXPLANATION-END].
- **Natural Language Question**: Translate the SQL query into a natural language question, enclosed within [QUESTION-START] and [QUESTION-END].
- **External Knowledge**: Include any relevant external knowledge if applicable, enclosed within [EXTERNAL-KNOWLEDGE-START] and [EXTERNAL-KNOWLEDGE-END]. Leave this section blank if not needed.'''

output_format_multi_round = '''Please structure your response as follows:

[EXPLANATION-START]
(SQL Explanation)
[EXPLANATION-END]

[QUESTION-START]
(Natural Language Question, in the format of [{"User": ...}, {"Assistant": ...}, {"User": ...}, ....])
[QUESTION-END]

- **SQL Explanation**: Provide a clear and detailed explanation of the SQL query, enclosed within [EXPLANATION-START] and [EXPLANATION-END].
- **Natural Language Question**: Convert the SQL query into a multi-round dialogue, enclosed within [QUESTION-START] and [QUESTION-END]. Represent this as a list that captures multiple rounds of conversation between the User and the Assistant.'''

instruction_wo_ek = "Based on the above information, follow the reasoning steps to generate the explanation and the question corresponding to the SQL query."

instruction_w_ek = "Based on the above information, follow the reasoning steps to generate the explanation, the question, and the external knowledge corresponding to the SQL query."

instruction_multi_round = "Based on the above information, follow the reasoning steps to generate the explanation and the dialogue corresponding to the SQL query."

def obtain_db_schema(db_file_dir):
    conn = sqlite3.connect(db_file_dir)
    cursor = conn.cursor()

    cursor.execute("SELECT name, sql FROM sqlite_master WHERE type='table';")
    tables = cursor.fetchall()

    table_names = []
    create_statements = []
    for table in tables:
        table_name, create_statement = table
        table_names.append(table_name)
        create_statements.append(create_statement)

    cursor.close()
    conn.close()

    return table_names, create_statements

# NOTE: When columns with the same names exist in different tables, more detailed design considerations are necessary
def extract_column_descriptions(create_statements):
    column_name2column_desc = dict()
    # Regular expression to match column definitions
    pattern = r'"(\w+)"\s+\w+\s*/\*\s*(.*?)\s*\*/'

    for create_statement in create_statements:
        # Find all matches in the string
        matches = re.findall(pattern, create_statement)

        # Print the results
        for column_name, description in matches:
            column_name = column_name.lower()
            if column_name not in column_name2column_desc:
                column_name2column_desc[column_name] = description

    return column_name2column_desc

if __name__ == "__main__":
    random.seed(42)
    db_path = "../database_synthesis/synthetic_sqlite_databases"
    sql_infos = json.load(open("../sql_synthesis/results/synthetic_sqls.json"))
    question_synthesis_template = open("./prompt_templates/question_synthesis_prompt.txt").read()
    styles = ["Formal", "Colloquial", "Imperative", "Interrogative", "Descriptive", "Concise", "Vague", "Metaphorical", "Multi-turn Dialogue"]

    print(sql_infos[0])
    db_ids = list(set([sql["db_id"] for sql in sql_infos]))
    print(len(db_ids))

    db_id2column_info = dict()
    for db_id in tqdm(db_ids):
        table_names, create_statements = obtain_db_schema(os.path.join(db_path, db_id, db_id + ".sqlite"))
        db_id2column_info[db_id] = extract_column_descriptions(create_statements)
    
    prompts = []
    for sql_info in tqdm(sql_infos):
        style_name = random.sample(styles, 1)[0]
        column_name2column_desc = db_id2column_info[sql_info["db_id"]]
        used_column_name2column_desc = dict()
        for column_name, column_desc in column_name2column_desc.items():
            if column_name.lower() in sql_info["sql"].lower():
                used_column_name2column_desc[column_name] = column_desc

        if style_name in ["Vague", "Metaphorical"]: # "Vague" and "Metaphorical" styles require external knowledge
            steps = steps_w_ek
            guidelines = guidelines_w_ek
            instruction = instruction_w_ek
            output_format = output_format_w_ek
        elif style_name == "Multi-turn Dialogue": # the "Multi-turn Dialogue" style uses a special multi-round format
            steps = steps_multi_round
            guidelines = guidelines_multi_round
            instruction = instruction_multi_round
            output_format = output_format_multi_round
        else:
            steps = steps_wo_ek
            guidelines = guidelines_wo_ek
            instruction = instruction_wo_ek
            output_format = output_format_wo_ek

        prompt = question_synthesis_template.format(
            style_desc = style2desc[style_name].strip(),
            engine = "SQLite",
            column_info = json.dumps(used_column_name2column_desc, indent = 2, ensure_ascii = False).strip(),
            sql = sql_info["sql"].strip(),
            steps = steps.strip(),
            guidelines = guidelines.strip(),
            output_format = output_format.strip(),
            instruction = instruction.strip()
        )
        
        sql_info["style"] = style_name
        sql_info["prompt"] = prompt
    
    with open("prompts/question_synthesis_prompts.json", "w", encoding="utf-8") as f:
        f.write(json.dumps(sql_infos, indent=2, ensure_ascii=False))
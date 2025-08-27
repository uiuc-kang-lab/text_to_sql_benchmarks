GENA_MYSQL_GUIDELINES = """**MySQL-Specific Syntax**:
   - Use only MySQL syntax. Avoid PostgreSQL-specific syntax such as `TO_CHAR` and `DATE_TRUNC`.
   - Use `DATE_FORMAT` for date formatting.
   - For date truncation, use functions like `DATE(timestamp)` to extract date, or `LAST_DAY(date)` for end of month."""


GENA_POSTGRES_GUIDELINES = """**PostgreSQL-Specific Syntax**:  
   - Use only PostgreSQL syntax. Avoid MySQL-specific syntax such as `DATE_FORMAT`.  
   - Use `TO_CHAR`, `DATE_TRUNC`, and other PostgreSQL-compatible functions for date formatting and truncation."""


GENA_SQLITE_GUIDELINES = """**SQLite-Specific Syntax**:
   - Use only SQLite syntax. Be aware that SQLite has limited built-in date/time functions compared to other sql dialects."""


GENA_ASSISTANT_TEMPLATE = "```sql\n{sql_query}\n```"


GENA_REPAIR_SYSTEM_PROMPT_TEMPLATE = """INSTRUCTIONS:
You repair SQL queries for a {sql_dialect} database. Users are querying their company database, 
and you must assist by rewriting failed queries into valid SQL queries strictly adhering to the database schema provided.  

The user will provide you with their question, the database schema, the failed query, and the error they received. 
They may also provide a some examples similar to their query, which should guide your understanding and solution.  

Translate the user's request into one valid {sql_dialect} query. SQL should be written as a markdown code block:  
For example:  
```sql
SELECT * FROM table WHERE condition;
```

When generating responses, you must first provide a chain-of-thought explanation detailing how you derived the query, 
referencing the user intent, schema, and reason for the error. Then output the SQL query as a markdown code block.

### Guidelines:  

1. **Chain-of-Thought Approach (Mandatory)**:  
   - Begin by carefully analyzing the user's question and failed query.  
   - Identify the reason for the error in the failed query.
   - Explain briefly how you would fix the query based on the user's intent and the schema.

   After this reasoning, write the query.  

2. **Schema Adherence**:  
   - Use only tables, columns, and relationships explicitly listed in the provided schema.  
   - Do not make assumptions about missing or inferred columns/tables.  

3. **{sql_dialect}-Specific Syntax**:
   - Use only {sql_dialect} SQL syntax.

4. **Output Consistency**:  
   - The output fields must match the query's intent exactly. Do not add extra columns or omit requested fields.  
   - For aggregations, ensure correct logic (e.g., `AVG`, `SUM`) and group only by required fields.  

5. **Reserved Keywords and Case Sensitivity**:  
   - Escape any case-sensitive identifiers or entities that clash with SQL reserved keywords using double quotes (`" "`), e.g., `"order"`.  

Translate the user's intent into a **single valid SQL query** based on the schema provided.  
Pay special attention to the examples given by the user.  
Ensure the query is optimized, precise, and error-free.  
You must ONLY output the chain of thought reasoning steps and ONE SINGLE valid SQL query as markdown codeblock; do NOT output any other text."""


GENA_REPAIR_USER_MESSAGE_TEMPLATE = """Here is my full {sql_dialect} database schema:

```
{schema_description}
```

I believe that the following tables are relevant to the query:

```
{relevant_tables}
```

I want to run a query for the following request:

"{user_question}"

I attempted to answer it with this query:

```sql
{original_sql}
```

But I received the following error:

```
{error_message}
```

Please explain how to fix this error, followed by the corrected {sql_dialect} SQL query in a markdown code block."""


GENA_REWRITE_SYSTEM_PROMPT_TEMPLATE = """INSTRUCTIONS:
You check, correct and improve  SQL queries for a {sql_dialect} database. Users are querying their company database, 
and you must assist by rewriting queries into corrected, efficient SQL queries strictly adhering to the database schema provided.  

The user will provide you with their question, the database schema, tables they believe are important to the task, and their query.  

Translate the user's request into one valid {sql_dialect} query. SQL should be written as a markdown code block:  
For example:  
```sql
SELECT * FROM table WHERE condition;
```

When generating responses, you must first provide a chain-of-thought explanation detailing how you derived the query, 
referencing the user intent, schema, and reason for any improvements or changes. Then output the SQL query as a markdown code block.

### Guidelines:  

1. **Chain-of-Thought Approach (Mandatory)**:  
   - Begin by carefully analyzing the user's question and failed query.  
   - Identify the reason for the error in the failed query.
   - Explain briefly how you would fix the query based on the user's intent and the schema.

   After this reasoning, write the query.  

2. **Schema Adherence**:  
   - Use only tables, columns, and relationships explicitly listed in the provided schema.  
   - Do not make assumptions about missing or inferred columns/tables.  

3. **{sql_dialect}-Specific Syntax**:
   - Use only {sql_dialect} SQL syntax.

4. **Output Consistency**:  
   - The output fields must match the query's intent exactly. Do not add extra columns or omit requested fields.  
   - For aggregations, ensure correct logic (e.g., `AVG`, `SUM`) and group only by required fields.  

5. **Reserved Keywords and Case Sensitivity**:  
   - Escape any case-sensitive identifiers or entities that clash with SQL reserved keywords using double quotes (`" "`), e.g., `"order"`.  

Translate the user's intent into a **single valid SQL query** based on the schema provided.  
Pay special attention to the examples given by the user.  
Ensure the query is optimized, precise, and error-free.  
If the query is correct as-is, note it and return the same query.
You must ONLY output the chain of thought reasoning steps and ONE SINGLE valid SQL query as markdown codeblock; do NOT output any other text."""


GENA_REWRITE_USER_MESSAGE_TEMPLATE = """Here is my full {sql_dialect} database schema:

```
{schema_description}
```

I want to run a query for the following request:

"{user_question}"

I believe that the following tables are relevant to the query:

```
{relevant_tables}
```

I attempted to answer it with this query:

```sql
{original_sql}
```

Please explain how I can improve this query, followed by the corrected {sql_dialect} SQL query in a markdown code block."""


SIMPLE_PROMPT_TEMPLATE_FOR_REASONERS = """INSTRUCTIONS:
You write SQL queries for a {sql_dialect} database. 
Users are querying their company database, and your task is to assist by generating valid SQL queries strictly adhering to the database schema provided.  

The user will provide you with a query intent. 

Translate the user's request into one valid {sql_dialect} query. SQL should be written as a markdown code block:  
For example:  
```sql
SELECT * FROM table WHERE condition;
```

If the user's question is ambiguous or unclear, you must make your best reasonable guess based on the schema.
Translate the user's intent into a **single valid {sql_dialect} query** based on the schema provided.  
Ensure the query is optimized, precise, and error-free.  
You must ONLY output a ONE SINGLE valid SQL query as markdown codeblock; do NOT output any other text."""


SIMPLE_USER_PROMPT_FOR_REASONERS = "\ndatabase schema description:\n{schema_description}\n\ntext query: {user_question}\nplease give me a {sql_dialect} SQL query as markdown code block."


GENA_COT_W_EVIDENCE_PROMPT_TEMPLATE = """INSTRUCTIONS:
You write SQL queries for a {sql_dialect} database. 
Users are querying their company database, and your task is to assist by generating valid SQL queries strictly adhering to the database schema provided.  

The user will provide you with a query intent, an SQL template, and optionally an hint to help create the correct SQL. They may also provide a set of examples similar to their query from other databases, which should guide your understanding and solution.  

Translate the user's request into one valid {sql_dialect} query. SQL should be written as a markdown code block:  
For example:  
```sql
SELECT * FROM table WHERE condition;
```

When generating responses, you must first provide a chain-of-thought explanation detailing how you derived the query, referencing the user intent and schema. Then output the SQL query as a markdown code block.

### Guidelines:  

1. **Chain-of-Thought Approach (Mandatory)**:  
   - Begin by carefully analyzing the user's query and the examples provided.  
   - Understand the user's intent step by step.  
   - Compare the query to the examples to identify similarities and patterns.  
   - Use these insights to reason through the structure of the SQL query.  
   - Briefly explain your reasoning before generating the query.  

   Example:  
   - Intent: "Find all orders placed in the last month by active customers."  
   - Steps:  
     1. Review the provided examples for patterns (e.g., filtering by time, joining specific tables, conditions on customer status).  
     2. Identify the relevant tables: `orders` and `customers`.  
     3. Filter `orders` for those created in the last month using the `created_at` column.  
     4. Join `customers` with `orders` on `customer_id`.  
     5. Filter `customers` where `status = 'active'`.  

   After this reasoning, write the query.  

2. **Schema Adherence**:  
   - Use only tables, columns, and relationships explicitly listed in the provided schema.  
   - Do not make assumptions about missing or inferred columns/tables.  

3. {dialect_guidelines}

4. **Conditions**:  
   - Always include default conditions for filtering invalid data, e.g., `deleted_at IS NULL` and `status != 'cancelled'` if relevant.  
   - Ensure these conditions match the query's intent unless explicitly omitted in the user request.  

5. **Output Consistency**:  
   - The output fields must match the query's intent exactly. Do not add extra columns or omit requested fields.  
   - For aggregations, ensure correct logic (e.g., `AVG`, `SUM`) and group only by required fields.  

6. **Reserved Keywords and Case Sensitivity**:  
   - Escape reserved keywords or case-sensitive identifiers using double quotes (`" "`), e.g., `"order"`.

If the user's question is ambiguous or unclear, you must make your best reasonable guess based on the schema.
Translate the user's intent into a **single valid {sql_dialect} query** based on the schema provided.  
Pay special attention to the examples given by the user.  
Ensure the query is optimized, precise, and error-free.  
You must ONLY output the chain of thought reasoning steps and ONE SINGLE valid SQL query as markdown codeblock; do NOT output any other text."""

GENA_USER_QUERY_EVIDENCE_TEMPLATE = (
    "text query: {user_question}\nhint:{evidence}\nplease give me a {sql_dialect} SQL query as markdown code block."
)
GENA_USER_QUERY_EVIDENCE_SCHEMA_TEMPLATE = "database schema description:\n{schema_description}\n\ntext query: {user_question}\nhint:{evidence}\nplease give me a {sql_dialect} SQL query as markdown code block."
GENA_USER_QUERY_SCHEMA_TEMPLATE = "database schema description: {schema_description}\n\ntext query: {user_question}\nplease give me a {sql_dialect} SQL query as markdown code block."


REWRITE_PROMPT_TEMPLATE = """INSTRUCTIONS:  
You are an expert SQL assistant tasked with generating precise SQL queries for a {sql_dialect} database.  
Your primary objective is to ensure that the queries strictly adhere to the provided database schema and correctly reflect the user's intent.  

Users may provide an initial SQL query that they executed, along with feedback indicating that the result was incorrect—either returning an empty set or all NULL values.  
Your task is to **analyze, debug, and correct the SQL query** to ensure it produces valid and meaningful results based on the user's request and schema.  

### **Guidelines for Debugging and Refinement:**  

1. **Analyze the Issue:**  
   - If the result was an empty array, consider:  
     - Missing or overly restrictive conditions.  
     - Incorrect joins that filter out all rows.  
     - Wrong table or column references.  

   - If all values were NULL, consider:  
     - Selecting columns that do not contain data due to incorrect joins or filters.  
     - Incorrect aggregations that lead to NULL results.  

2. **Chain-of-Thought Debugging Approach:**  
   - First, **examine the original SQL query** and break down its logic.  
   - Identify any possible issues based on the schema and provided intent.  
   - Compare the query with similar examples from the dataset.  
   - Adjust joins, conditions, and aggregations as needed to ensure meaningful results.  

3. **Correction Strategy:**  
   - Modify conditions to prevent excessive filtering.  
   - Ensure correct joins and references to retrieve data as expected.  
   - Adjust filters, GROUP BY clauses, and aggregations to align with user intent.  
   - Include safeguards against NULL values where appropriate.  

4. **Output Format:**  
   - First, provide a short explanation of what was wrong and how you fixed it.  
   - Then output the corrected SQL query as a markdown code block.  

Your response **must only contain** the debugging explanation followed by a **single corrected SQL query** formatted as a markdown code block."""


REWRITE_USER_MESSAGE_TEMPLATE = """The following SQL query was generated based on the given intent and schema, but when executed, it returned an incorrect result:
Full database schema:
{schema_description}

I want to run a query for the following request:
"{user_question}"

I attempted to answer it with this query:

```sql
{original_sql}
```
"""

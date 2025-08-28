API_KEYS = ""

model_openai = "gpt-4o"

# Let the sql be written in one line.
SQL_FORMAT_PROMPT = """Please write the above sql in one line with no extra information, just one sql statement. Follow the format below:

SQL: SELECT song_name ,  song_release_year FROM singer ORDER BY age LIMIT 1;"""


SQL_EXECUTE_OUTPUT_CORRECT_PROMPT = """The result of the above sql execution is as follows:\n"""

SQL_EXECUTE_OUTPUT_CORRECT_PROMPT_CHECK_OUTPUT_back_part_1 = """Please analyze whether the given SQL query meets the following requirements and whether its execution result is reasonable.

### Step 1: Requirement Check
- Confirm whether the SQL query aligns with the requirement specified in ###Input.
- Keep an eye on ###Hint for information that is a reference to help you check your SQL, based on the information provided in ###Hint, verify if the SQL query correctly understands and applies the relevant concepts or constraints.
- One situation requires special attention. If you think that the parts related to values in the SQL do not match the ###Hint, please clearly state the relevant value_sample from the ###Value Example. When making corrections to the values, please base them on the value_sample rather than the ###Hint.

### Step 2: Result Reasonableness
- Analyze whether the execution result of the SQL query matches the expected outcome and satisfies the requirements in ###Input.
- If the SQL involves arithmetic operations, check that the data types in the arithmetic operations section are correct, and write your analysis in a descriptive manner.
- If the SQL execution result is empty, it indicates an issue with the query, as the database is guaranteed to contain data that satisfies the ###Input requirements. In such cases, adjust the SQL query to ensure it meets the requirements and returns a valid result.

### Guidelines
- If the SQL query already meets the requirements in `###Input` and `###Hint` and produces a reasonable result, no changes are needed.
- If it does not meet the requirements, modify the SQL query to ensure it fulfills all requirements and generates a logical and reasonable result.
- Clearly write out the final corrected SQL in the format below, without using any other format. Format:
###SQL: SELECT song_name, song_release_year FROM singer ORDER BY age LIMIT 1; ###END"""

SQL_EXECUTE_OUTPUT_CORRECT_PROMPT_CHECK_OUTPUT_back_part_2 = """Please analyze whether the given SQL query meets the following requirements and whether its execution result is reasonable.

### Step 1: Requirement Check
- Confirm whether the SQL query aligns with the requirement specified in ###Input.

### Step 2: Result Reasonableness
- Analyze whether the execution result of the SQL query matches the expected outcome and satisfies the requirements in ###Input.
- If the SQL involves arithmetic operations, check that the data types in the arithmetic operations section are correct, and write your analysis in a descriptive manner.
- If the SQL execution result is empty, it indicates an issue with the query, as the database is guaranteed to contain data that satisfies the ###Input requirements. In such cases, adjust the SQL query to ensure it meets the requirements and returns a valid result.

### Guidelines
- If the SQL query already meets the requirements in `###Input` and produces a reasonable result, no changes are needed.
- If it does not meet the requirements, modify the SQL query to ensure it fulfills all requirements and generates a logical and reasonable result.
- Clearly write out the final corrected SQL in the format below, without using any other format. Format:
###SQL: SELECT song_name, song_release_year FROM singer ORDER BY age LIMIT 1; ###END"""
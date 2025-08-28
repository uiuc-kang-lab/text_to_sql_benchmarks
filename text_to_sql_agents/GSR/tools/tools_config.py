###extractor###
FEW_SHOT = """Please help me extract the tables and columns involved in the following SQL statement, then list them. When listing, do not use aliases, and the column names should be enclosed in double quotes. Here are some examples, please follow the format of the examples for output. 

###Example 1: 
Input: 
SELECT MAX("Free Meal Count (K-12)" * 1.0 / "Enrollment (K-12)") AS highest_eligible_free_rate FROM frpm WHERE "County Name" = 'Alameda';
Output:
{Table frpm:
columns:"Free Meal Count (K-12)","Enrollment (K-12)","County Name"}

###Example 2: 
Input: 
SELECT COUNT(*) FROM satscores s JOIN schools sch ON s.cds = sch.CDSCode WHERE s.AvgScrMath > 400 AND sch.Virtual = 'F';
Output:
{Table satscores:
columns:"cds","AvgScrMath"},
{Table schools:
columns:"CDSCode","Virtual"}

"""

KEYWORD_EXTRACT_FEW_SHOT = """Based on the following natural language description and SQL query, extract condition values related to the columns specified in ###Columns only.
1. ###Text is the natural language description of the query requirements.
2. ###SQL is the SQL query.
3. ###Columns lists only the columns for which we need condition values.

###Instructions:
1. When identifying condition values, focus on extracting the complete keyword information from the natural language description.
2. Since keywords can sometimes serve as both column names and values, extract the full keyword or phrase that may act as a value, especially if it appears to convey descriptive context.
3. Please extract condition values for the columns specified in ###Columns only, ignoring any other columns.
###Output format:
1. Analyze each column listed in ###Columns, and identify the relevant keywords in the natural language description,  extracting them as complete values.
2. Return a dictionary structure with each column name paired with its corresponding condition value in the format:
{column1: "condition value1", column2: "condition value2"}
3. Please do not use another format.

Example1:
###Text: How many schools in merged Alameda have number of test takers less than 100?
###SQL: SELECT COUNT(*) FROM satscores WHERE cname = 'Alameda' AND NumTstTakr < 100;
###Columns: "cname", "NumTstTakr"

###Output: {"cname": "merged Alameda", "NumTstTakr": "less than 100"}

Example2:
###Text: What is the educational level name for the schools with Breakfast Provision 2 in county code 37? Indicate the name of the school.
###SQL: SELECT s.School, s.EILName FROM schools s JOIN frpm f ON s.CDSCode = f.CDSCode WHERE f."NSLP Provision Status" = '2' AND f."County Code" = '37';
###Columns: "NSLP Provision Status", "County Code"

###Output: {"NSLP Provision Status": "Breakfast Provision 2", "County Code":"37"}

"""
########################################


###format_masked_regenerate_schema###
HINT_SQL_REGENERATE_SYMBOL_FORMAT_PROMPT = """You are a database expert. Your task is to help me extract the tables and columns related to the ###Input from the ###Database Schema, based on the following components: ###Database Schema, ###Input, ###Hint.

Each section provides specific information:
###Database Schema: Details the structure of the database, including tables and columns.
###Input: Specifies the data the user wants to query, including required columns and conditions.
###Hint: Provides additional context or constraints related to the ###Input.

Please follow the steps below and write down each step of the process: 
1. You need to understand exactly what ###Input needs.
2. Please based on the column_description of the columns of each table, I need you to help me find the columns related to ###Input as per the requirement. For each table, you need to find 3 to 5 columns that may be related to ###Input. Note that each table is required.
3. Please list the columns that you think are related to the ###Input in the format below. For each table, you need to list 3 to 5 columns that may be relevant, even if they are not. Please do not use another format, return only what is in the format below, no additional information. Format:
###Related Schema
{Table satscores:
columns:"cds","AvgScrMath"},
{Table schools:
columns:"CDSCode","Virtual"}
###END"""

NO_HINT_SQL_REGENERATE_SYMBOL_FORMAT_PROMPT = """You are a database expert. Your task is to help me extract the tables and columns related to the ###Input from the ###Database Schema, based on the following components: ###Database Schema, ###Input. 

Each section provides specific information:
###Database Schema: Details the structure of the database, including tables and columns.
###Input: Specifies the data the user wants to query, including required columns and conditions.

Please follow the steps below and write down each step of the process: 
1. You need to understand exactly what ###Input needs.
2. Please based on the column_description of the columns of each table, I need you to help me find the columns related to ###Input as per the requirement. For each table, you need to find 3 to 5 columns that may be related to ###Input. Note that each table is required.
3. Please list the columns that you think are related to the ###Input in the format below. For each table, you need to list 3 to 5 columns that may be relevant, even if they are not. Please do not use another format, return only what is in the format below, no additional information. Format:
### Related Schema
{Table satscores:
columns:"cds","AvgScrMath"},
{Table schools:
columns:"CDSCode","Virtual"}
### END"""

# HINT_SQL_REGENERATE_SYMBOL_FORMAT_PROMPT = """You are a database expert. Your task is to help me extract the tables and columns related to the ###Input from the ###Database Schema, based on the following components: ###Database Schema, ###Input, ###Hint, ###Logic Clause.
#
# Each section provides specific information:
# ###Database Schema: Details the structure of the database, including tables and columns.
# ###Input: Specifies the data the user wants to query, including required columns and conditions.
# ###Hint: Provides additional context or constraints related to the ###Input.
# ###Logic Clause: This is meant to help you better understand the ###Input.
#
# Please follow the steps below and write down each step of the process:
# 1. You need to understand exactly what ###Input needs based on the logic clause.
# 2. Please based on the column_description of the columns of each table, I need you to help me find the columns related to ###Input as per the requirement. For each table, you need to find 3 to 5 columns that may be related to ###Input. Note that each table is required.
# 3. Please list the columns that you think are related to the ###Input in the format below. For each table, you need to list 3 to 5 columns that may be relevant, even if they are not. Please do not use another format, return only what is in the format below, no additional information. Format:
# ###Related Schema
# {Table satscores:
# columns:"cds","AvgScrMath"},
# {Table schools:
# columns:"CDSCode","Virtual"}
# ###END"""
#
# NO_HINT_SQL_REGENERATE_SYMBOL_FORMAT_PROMPT = """You are a database expert. Your task is to help me extract the tables and columns related to the ###Input from the ###Database Schema, based on the following components: ###Database Schema, ###Input, ###Logic Clause.
#
# Each section provides specific information:
# ###Database Schema: Details the structure of the database, including tables and columns.
# ###Input: Specifies the data the user wants to query, including required columns and conditions.
# ###Logic Clause: This is meant to help you better understand the ###Input.
#
# Please follow the steps below and write down each step of the process:
# 1. You need to understand exactly what ###Input needs based on the logic clause.
# 2. Please based on the column_description of the columns of each table, I need you to help me find the columns related to ###Input as per the requirement. For each table, you need to find 3 to 5 columns that may be related to ###Input. Note that each table is required.
# 3. Please list the columns that you think are related to the ###Input in the format below. For each table, you need to list 3 to 5 columns that may be relevant, even if they are not. Please do not use another format, return only what is in the format below, no additional information. Format:
# ### Related Schema
# {Table satscores:
# columns:"cds","AvgScrMath"},
# {Table schools:
# columns:"CDSCode","Virtual"}
# ### END"""
########################################
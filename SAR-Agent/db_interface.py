import snowflake.connector
import json
import sqlite3

def read_snowflake_query(query: str, database_id: str, explaination: str,instance_id: str,):
    with open(f'./analyze_result/{instance_id}/query_result.txt', 'a') as f:
        f.write(f'Query: {query}\n')
    with open(f'./analyze_result/{instance_id}/query_result.txt', 'a') as f:
        f.write(f'Explaination of the query: {explaination}\n')
    with open('./snowflake_credential.json', 'r') as f:
        credential = json.load(f)
    try:
        conn = snowflake.connector.connect(
            database=database_id,
            **credential
        )
        cursor = conn.cursor()
        cursor.execute(query)
        result = cursor.fetchall()
        cursor.close()
        conn.close()
        with open(f'./analyze_result/{instance_id}/query_result.txt', 'a') as f:
            f.write(f'Result: {result}\n')
        return result
    except Exception as e:
        with open(f'./analyze_result/{instance_id}/query_result.txt', 'a') as f:
            f.write(f'Error: {e}\n')
        return e

def read_sqlite_query(query: str, explaination: str, database_id: str, instance_id: str):
    with open(f'./analyze_result/{instance_id}/query_result.txt', 'a') as f:
        f.write(f'Query: {query}\n')
    with open(f'./analyze_result/{instance_id}/query_result.txt', 'a') as f:
        f.write(f'Explaination of the query: {explaination}\n')
    try:
        conn = sqlite3.connect(f'./bird/dev_databases/{database_id}/{database_id}.sqlite')
        cursor = conn.cursor()
        cursor.execute(query)
        result = cursor.fetchall()
        cursor.close()
        conn.close()
        with open(f'./analyze_result/{instance_id}/query_result.txt', 'a') as f:
            f.write(f'Result: {result}\n')
    except Exception as e:
        with open(f'./analyze_result/{instance_id}/query_result.txt', 'a') as f:
            f.write(f'Error: {e}\n')
        return e
    return result

def terminate(analyze_result: str, instance_id: str):
    with open(f'./analyze_result/{instance_id}/final_analyze_result.txt', 'w') as f:
        f.write(analyze_result)
    return "Terminate"

def get_function_call():
    functions = [
        {
            "name": "read_snowflake_query",
            "description": "Read the result of a snowflake query",
            "parameters": {
                "type": "object",
                "properties": {
                    "query": {
                        "type": "string",
                        "description": "The snowflake query to read the result of."
                    },
                    "database_id": {
                        "type": "string",
                        "description": "The database to read the result of."
                    },
                    "explaination": {
                        "type": "string",
                        "description": "The explaination of the query you are going to execute."
                    }
                },
                "required": ["query", "database_id", "explaination"]
            }
        },
        {
            "name": "terminate",
            "description": "The agent is done with the task and should terminate.",
            "parameters": {
                "type": "object",
                "properties": {
                    "analyze_result": {
                        "type": "string",
                        "description": "The analyze result of the query."
                    }
                },
                "required": ["analyze_result"]
            }
        }
    ]

    
    return functions


def get_function_call_bird():
    functions = [
        {
            "name": "read_sqlite_query",
            "description": "Read the result of a sqlite query",
            "parameters": {
                "type": "object",
                "properties": {
                    "query": {
                        "type": "string",
                        "description": "The sqlite query to read the result of."
                    },
                    "explaination": {
                        "type": "string",
                        "description": "The explaination of the query you are going to execute."
                    }
                },
                "required": ["query", "explaination"]
            }
        },
        {
            "name": "terminate",
            "description": "The agent is done with the task and should terminate.",
            "parameters": {
                "type": "object",
                "properties": {
                    "analyze_result": {
                        "type": "string",
                        "description": "The analyze result of the query."
                    }
                },
                "required": ["analyze_result"]
            }
        }
    ]

    
    return functions



def post_process(message: str, instance_id: str, database_id: str = None):
    function_list = {
        "read_snowflake_query": read_snowflake_query,
        "read_sqlite_query": read_sqlite_query,
        "terminate": terminate
    }
    if message.function_call:
        function_name = message.function_call.name
        arguments = json.loads(message.function_call.arguments)
        if function_name == "terminate":
            result = function_list[function_name](arguments["analyze_result"], instance_id)
        else:
            result = function_list[function_name](arguments["query"], arguments["explaination"], database_id, instance_id)

        # Print the result
        return result
    else:
        # Print direct response
        return message.content
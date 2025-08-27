import json
import pandas as pd

def get_prompt(data: dict, single: bool = False):
    prompt_file = "./prompts/prompt_user_sf.txt"
    with open(prompt_file, "r") as f:
        prompt = f.read()
    question = data['instruction']
    instance_id = data['instance_id']

    with open(f'./spider2/gold_schema/{instance_id}/full_schema.json', 'r') as f:
        full_schema = json.load(f)
    schema = '\n'.join([f"{k}: {v}" for k, v in full_schema.items()])
    external_knowledge_file = data['external_knowledge']
    if data['external_knowledge'] is None:
        external_knowledge = ''
    else:
        with open(f'./spider2/gold_schema/{instance_id}/{external_knowledge_file}', 'r') as f:
            external_knowledge = f.read()
    
    with open(f'./spider2/sql/{instance_id}.sql', 'r') as f:
        sql_query = f.read()


    input_prompt = prompt.format(question=question, schema=schema, external_knowledge=external_knowledge, gold_query=sql_query)
    return input_prompt


def get_prompt_bird(data: dict, single: bool = False):
    prompt_file = "./prompts/prompt_user_bird.txt"
    with open(prompt_file, "r") as f:
        prompt = f.read()
    question = data['question']
    db_name = data['db_id']
    
    question = data['question']
    gold_query = data['SQL']
    external_knowledge = data['evidence']
    with open(f'./data_minidev/MINIDEV/dev_databases/{db_name}/full_schema.json', 'r') as f:
        full_schema = json.load(f)
    schema = '\n'.join([f"{k}: {v}" for k, v in full_schema.items()])
    input_prompt = prompt.format(question=question, schema=schema, external_knowledge=external_knowledge, gold_query=gold_query)
    return input_prompt

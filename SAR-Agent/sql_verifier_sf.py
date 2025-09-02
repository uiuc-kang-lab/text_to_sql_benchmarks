"""
SQL Query Generation Agent Framework

This module implements an agent-based approach to generate SQL queries by breaking down
complex queries into subqueries and generating them step by step.
"""

import os
import json
import logging
from typing import Dict, List, Any, Optional, Set, Tuple, Callable
from openai import OpenAI
from datetime import datetime
import pandas as pd
from llm_interface import LLMInterface
import random
from prompt_preprocess import get_prompt, get_prompt_bird
from db_interface import get_function_call,get_function_call_bird,post_process
import argparse

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(f'logs/query_generation_{datetime.now().strftime("%Y%m%d_%H%M%S")}.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)
    
        

class SARAgent:
    """
    An agent that generates SQL queries by decomposing complex queries into
    subqueries and generating them step by step.
    """
    
    def __init__(self, model: str, api_key: str, prompt: str, functions: List[Dict[str, Any]]):
        self.api_key = api_key
        self.llm = LLMInterface(model, prompt, api_key, functions)


    def generate_query(self, messages) -> Tuple[bool, str]:
        """Determine if the query needs to be broken down into subqueries"""
        response = self.llm.call(message=messages)
        return response
    
    def get_total_cost(self) -> float:
        """Get the total cost of all API calls made through this interface."""
        return self.llm.get_total_cost()

def get_data_list(old_sf: bool = False):
    data_list = []
    processed_data_list = []
    for file in os.listdir('./spider2/sql'):
        data_list.append(file.split('.')[0])
        
    question_list = {}
    file_name = './spider2/spider2-snow.jsonl'
    if old_sf:
        file_name = './spider2/spider2-snow-0713.jsonl'
    with open(file_name, 'r') as f:
        for line in f:
            data = json.loads(line)
            question_list[data['instance_id']] = data
    for instance_id in data_list:
        processed_data_list.append(question_list[instance_id])
    return processed_data_list

def main():
    # Example usage
    model = 'o3'
    api_key = os.getenv("ANTHROPIC_API_KEY" if 'claude' in model.lower() else "OPENAI_API_KEY")
    
    # Initialize agent
    parser = argparse.ArgumentParser()
    parser.add_argument('--old_sf', action='store_true', help='Use old spider2-snow.jsonl')
    args = parser.parse_args()
    old_sf = args.old_sf
    gold_data_list = get_data_list(old_sf)
    gold_data_list.sort(key=lambda x: x['instance_id'])
    count = 0
    
    for data in gold_data_list:
        logger.info(f"Processing {count} th instance")
        count += 1
        if os.path.exists(f'./analyze_result/{data["instance_id"]}'):
            continue
        
        instance_id = data['instance_id']
        os.makedirs(f'./analyze_result/{instance_id}', exist_ok=True)

        input_prompt = get_prompt(data)
        logger.info(f"Generating query for {instance_id}")
        logger.info(f"Prompt: {input_prompt}")
        functions = get_function_call()
        agent = SARAgent(model, api_key, input_prompt, functions)
        user_input = 'Please judge the correctness and ambiguity of the query'
        for i in range(30):
            logger.info(f"Step {i}")
            message = agent.generate_query(user_input)
            result = post_process(message, instance_id, data['db_id'])
            logger.info(f"Message: {message}")
            logger.info(f"Result: {result}")
            if result == 'Terminate':
                break
            else:
                user_input = 'Query running result: ' + str(result)
        with open(f'./analyze_result/results.jsonl', 'a') as f:
            f.write(json.dumps({'instance_id': instance_id, 'cost': agent.get_total_cost(), 'step': i+1}))
            f.write('\n')




if __name__ == "__main__":
    main()

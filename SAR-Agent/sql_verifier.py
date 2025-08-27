"""
SQL Query Generation Agent Framework

This module implements an agent-based approach to generate SQL queries by breaking down
complex queries into subqueries and generating them step by step.
"""

import os
import json
import logging
from typing import Dict, List, Any, Optional, Set, Tuple, Callable
from dataclasses import dataclass
import anthropic
from openai import OpenAI
from datetime import datetime
import pandas as pd
from pydantic import BaseModel
from llm_interface import LLMInterface
import random
from prompt_preprocess import get_prompt, get_prompt_bird
from db_interface import get_function_call,get_function_call_bird,post_process

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
        print(73, response)
        return response
    
    def get_total_cost(self) -> float:
        """Get the total cost of all API calls made through this interface."""
        return self.llm.get_total_cost()



def main():
    # Example usage
    model = 'o3'
    api_key = os.getenv("ANTHROPIC_API_KEY" if 'claude' in model.lower() else "OPENAI_API_KEY")
    
    # Initialize agent

    data_list = []
    with open('./data_minidev/MINIDEV/mini_dev_sqlite.json', 'r') as f:
        data_list = json.load(f)
    data_list.sort(key=lambda x: x['question_id'])
    count = 0
    for data in data_list[400:]:
        logger.info(f"Processing {count} th instance")
        count += 1

        if os.path.exists(f'./analyze_result/{data["question_id"]}'):
            continue
        
        instance_id = data['question_id']
        os.makedirs(f'./analyze_result/{instance_id}', exist_ok=True)

        input_prompt = get_prompt_bird(data)
        logger.info(f"Generating query for {instance_id}")
        logger.info(f"Prompt: {input_prompt}")
        functions = get_function_call_bird()
        agent = SARAgent(model, api_key, input_prompt, functions)
        user_input = 'Please judge the correctness and ambiguity of the text-to-sql pair.'
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


        # logger.info(f"Correctness: {correctness}, Is_ambiguous: {is_ambiguous}, Explaination: {explaination}")
        with open(f'./analyze_result/results.jsonl', 'a') as f:
            f.write(json.dumps({'instance_id': instance_id, 'cost': agent.get_total_cost(), 'step': i+1}))
            f.write('\n')


if __name__ == "__main__":
    main()

import argparse
import json
import os
import re
import time
from json_repair import json_repair

def parse_response(response):
    schema_pattern = r'```json\s*([\s\S]*?)\s*```'

    try:
        enhanced_schema_match = re.search(schema_pattern, response, re.DOTALL)
        enhanced_schema_str = enhanced_schema_match.group(0).strip() if enhanced_schema_match else None
        enhanced_schema_dict = json_repair.loads(enhanced_schema_str)

        return enhanced_schema_dict
    except Exception as e:
        print(response)
        print("Parsing Exception:", str(e))
        return None

def parse_prompt(prompt):
    domain_pattern = r'(?<=\*\*Business Domain:\*\*)(.*?)(?=\*\*Business Scenario:\*\*)'
    scenario_pattern = r'(?<=\*\*Business Scenario:\*\*)(.*?)(?=\*\*Initial Database Schema:\*\*)'

    domain_match = re.search(domain_pattern, prompt, re.DOTALL)
    domain = domain_match.group(0).strip() if domain_match else None

    scenario_match = re.search(scenario_pattern, prompt, re.DOTALL)
    scenario = scenario_match.group(0).strip() if scenario_match else None

    return domain, scenario

def llm_inference(model, prompts):
    '''
    This function leverages a large language model (LLM) to generate responses for a given list of prompts.
    You can integrate your preferred LLM within this function.

    Args:
        model: The LLM to be used for inference.
        prompts: A list of prompts for which the LLM will generate responses.

    Returns:
        A list of dictionaries, each containing the original prompt, extracted domain and scenario, 
        and a JSON-formatted enhanced schema.
    '''
    
    # Generate responses using the LLM (each prompt corresponds to one response)
    responses = None  # Replace this with the actual LLM call, e.g., model.generate(prompts, temperature=0, n=1)


    # Initialize a list to store the processed results
    results = []

    # Iterate over prompts and their corresponding responses
    for prompt, response in zip(prompts, responses):
        # Parse the response to get the enhanced schema
        enhanced_schema_dict = parse_response(response)
        if enhanced_schema_dict is None:
            continue
        
        # Extract domain and scenario from the prompt
        domain, scenario = parse_prompt(prompt)

        # Append the results with structured data
        results.append({
            "prompt": prompt,
            "domain": domain,
            "scenario": scenario,
            "enhanced_schema": json.dumps(enhanced_schema_dict, indent=2, ensure_ascii=False)
        })

    return results

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("--model", type = str)
    args = parser.parse_args()
    
    print(args)

    prompts = json.load(open("./prompts/prompts_schema_enhancement.json"))
    output_file = "./results/schema_enhancement.json"
    results = llm_inference(args.model, prompts)

    with open(output_file, "w", encoding = "utf-8") as f:
        f.write(json.dumps(results, indent = 2, ensure_ascii = False))

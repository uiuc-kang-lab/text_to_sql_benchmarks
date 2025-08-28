import argparse
import json
import re
from tqdm import tqdm

def parse_response(response):
    pattern = r"```sql\s*(.*?)\s*```"
    
    sql_blocks = re.findall(pattern, response, re.DOTALL)

    if sql_blocks:
        # Extract the last SQL query in the response text and remove extra whitespace characters
        last_sql = sql_blocks[-1].strip()
        return last_sql
    else:
        print("No SQL blocks found.")
        return ""

def llm_inference(model, prompts, db_ids):
    """
    Generates responses using an LLM for given prompts.

    Args:
        model: The LLM to use for generating responses.
        prompts (list of str): A list of prompts for the model.
        db_ids (list of str): A list of database IDs corresponding to each prompt.

    Returns:
        list of dict: A list of dictionaries containing the prompt, db_id, and generated response.
    """
    
    # Replace with actual LLM call to generate responses
    # `responses` should be a list of strings (list of str), where each string is the LLM's output for a prompt.
    responses = None # model.generate(prompts, temperature=0.8, n=1), this is an example call, adjust as needed

    results = [
        {
            "prompt": prompt,
            "db_id": db_id,
            "response": response
        }
        for prompt, db_id, response in zip(prompts, db_ids, responses)
    ]

    return results

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("--model", type = str)

    opt = parser.parse_args()
    print(opt)

    input_dataset = json.load(open("./prompts/sql_synthesis_prompts.json"))
    output_file = "./results/sql_synthesis.json"

    db_ids = [data["db_id"] for data in input_dataset]
    prompts = [data["prompt"] for data in input_dataset]
    
    results = llm_inference(opt.model, prompts, db_ids)

    with open(output_file, "w", encoding = "utf-8") as f:
        f.write(json.dumps(results, indent = 2, ensure_ascii = False))
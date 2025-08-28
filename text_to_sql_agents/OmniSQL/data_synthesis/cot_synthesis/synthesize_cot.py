import argparse
import json
import argparse
import json

def llm_inference(model, dataset):
    """
    Perform LLM inference to generate multiple responses for each prompt in the dataset.

    Args:
        model: The LLM used for inference.
        dataset: A list of dictionaries.

    Returns:
        A list of dictionaries, where each dictionary includes the original data and the corresponding generated responses.
    """

    prompts = [data["cot_synthesis_prompt"] for data in dataset]

    # Placeholder for storing generated responses for each prompt
    # Each element in `responses_list` is a list of responses (strings) corresponding to a prompt.
    responses_list = []  # Replace this with your actual response generation logic.

    # Initialize an empty list to store the results
    results = []

    # Iterate through the dataset and the corresponding responses
    for data, responses in zip(dataset, responses_list):
        # Add the generated responses to the current data entry
        data["responses"] = responses

        # Append the updated data entry to the results
        results.append(data)

    return results

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("--model", type = str)

    opt = parser.parse_args()
    print(opt)

    input_dataset = json.load(open("./prompts/cot_synthesis_prompts.json"))
    output_file = "./results/cot_synthesis.json"
    
    results = llm_inference(opt.model, input_dataset)

    with open(output_file, "w", encoding = "utf-8") as f:
        f.write(json.dumps(results, indent = 2, ensure_ascii = False))

import argparse
import json
import re
from vllm import LLM, SamplingParams
from transformers import AutoTokenizer

def parse_response(response):
    pattern = r"```sql\s*(.*?)\s*```"
    
    sql_blocks = re.findall(pattern, response, re.DOTALL)

    if sql_blocks:
        # Extract the last SQL query in the response text and remove extra whitespace characters
        last_sql = sql_blocks[-1].strip()
        return last_sql
    else:
        # print("No SQL blocks found.")
        return ""

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("--pretrained_model_name_or_path", type = str, default = "/fs/fast/u2021000902/previous_nvme/xxx")
    parser.add_argument("--input_file", type = str, help = "the input file path (prompts)")
    parser.add_argument("--output_file", type = str, help = "the output file path (results)")
    parser.add_argument("--tensor_parallel_size", type = int, help = "the number of used GPUs", default = 4)
    parser.add_argument("--n", type = int, help = "the number of generated responses", default = 4)
    parser.add_argument("--temperature", type = float, help = "temperature of llm's sampling", default = 1.0)

    opt = parser.parse_args()
    print(opt)

    input_dataset = json.load(open(opt.input_file))
    tokenizer = AutoTokenizer.from_pretrained(opt.pretrained_model_name_or_path, trust_remote_code=True)
    
    if "Qwen2.5-" in opt.pretrained_model_name_or_path:
        stop_token_ids = [151645] # 151645 is the token id of <|im_end|> (end of turn token in Qwen2.5)
    elif "deepseek-coder-" in opt.pretrained_model_name_or_path:
        stop_token_ids = [32021]
    elif "DeepSeek-Coder-V2" in opt.pretrained_model_name_or_path:
        stop_token_ids = [100001]
    elif "OpenCoder-" in opt.pretrained_model_name_or_path:
        stop_token_ids = [96539]
    elif "Meta-Llama-" in opt.pretrained_model_name_or_path:
        stop_token_ids = [128009, 128001]
    elif "granite-" in opt.pretrained_model_name_or_path:
        stop_token_ids = [0] # <|end_of_text|> is the end token of granite-3.1 and granite-code
    elif "starcoder2-" in opt.pretrained_model_name_or_path:
        stop_token_ids = [0] # <|end_of_text|> is the end token of starcoder2
    elif "Codestral-" in opt.pretrained_model_name_or_path:
        stop_token_ids = [2]
    elif "Mixtral-" in opt.pretrained_model_name_or_path:
        stop_token_ids = [2]
    elif "OmniSQL-" in opt.pretrained_model_name_or_path:
        stop_token_ids = [151645] # OmniSQL uses the same tokenizer as Qwen2.5
    else:
        print("Use Qwen2.5's stop tokens by default.")
        stop_token_ids = [151645]

    print("stop_token_ids:", stop_token_ids)
    
    max_model_len = 8192 # used to allocate KV cache memory in advance
    max_input_len = 6144
    max_output_len = 2048 # (max_input_len + max_output_len) must <= max_model_len
    
    print("max_model_len:", max_model_len)
    print("temperature:", opt.temperature)
    sampling_params = SamplingParams(
        temperature = opt.temperature, 
        max_tokens = max_output_len,
        n = opt.n,
        stop_token_ids = stop_token_ids
    )

    llm = LLM(
        model = opt.pretrained_model_name_or_path,
        dtype = "bfloat16", 
        tensor_parallel_size = opt.tensor_parallel_size,
        max_model_len = max_model_len,
        gpu_memory_utilization = 0.92,
        swap_space = 42,
        enforce_eager = True,
        disable_custom_all_reduce = True,
        trust_remote_code = True
    )
    
    chat_prompts = [tokenizer.apply_chat_template(
        [{"role": "user", "content": data["input_seq"]}],
        add_generation_prompt = True, tokenize = False
    ) for data in input_dataset]

    outputs = llm.generate(chat_prompts, sampling_params)
    
    results = []
    for data, output in zip(input_dataset, outputs):
        responses = [o.text for o in output.outputs]
        sqls  = [parse_response(response) for response in responses]
        
        data["responses"] = responses
        data["pred_sqls"] = sqls
        results.append(data)

    with open(opt.output_file, "w", encoding = "utf-8") as f:
        f.write(json.dumps(results, indent = 2, ensure_ascii = False))

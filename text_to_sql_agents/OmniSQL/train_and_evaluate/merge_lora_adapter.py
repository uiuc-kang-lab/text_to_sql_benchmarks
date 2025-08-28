from transformers import AutoModelForCausalLM, AutoTokenizer
from peft import PeftModel
import torch

if __name__ == "__main__":
    model = AutoModelForCausalLM.from_pretrained(
        "Qwen/Qwen2.5-Coder-32B-Instruct", 
        torch_dtype = torch.bfloat16
    )
    tokenizer = AutoTokenizer.from_pretrained("Qwen/Qwen2.5-Coder-32B-Instruct")
    print(model.dtype)

    peft_model_id = "your_lora_weight_path"
    print(peft_model_id)
    model = PeftModel.from_pretrained(model, peft_model_id)

    print("before merging:")
    for name, param in model.named_parameters():
        print(name)

    model = model.merge_and_unload(progressbar = True)
    print(model.dtype)

    print("after merging:")
    for name, param in model.named_parameters():
        print(name)

    model.save_pretrained(
        peft_model_id + "-full-model", 
        max_shard_size = "4GB"
    )

    tokenizer.save_pretrained(
        peft_model_id + "-full-model"
    )

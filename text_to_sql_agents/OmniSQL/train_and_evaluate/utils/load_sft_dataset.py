import json
import torch
from torch.utils.data import Dataset
from tqdm import tqdm
import numpy as np

def find_sublist_index(lst, sublist):
    sublist_length = len(sublist)
    for i in range(len(lst) - sublist_length + 1):
        if lst[i:i + sublist_length] == sublist:
            return i
    return -1

def obtain_labels(input_ids, assistant_start_token_ids):
    '''
    Mask everything before assistant_start_token_ids with -100
    '''
    assistant_start_idx = find_sublist_index(input_ids, assistant_start_token_ids)
    if assistant_start_idx == -1:
        labels = input_ids
        print("length of the output sequence exceeds max length")
    else:
        labels = [-100] * assistant_start_idx + input_ids[assistant_start_idx: ]
    assert len(input_ids) == len(labels)

    return labels

class SFTDataset(Dataset):
    def __init__(self, data_dir, tokenizer, max_length, mode):
        super().__init__()
        self.mode = mode
        assistant_start_token_ids = [151644, 77091] # for Qwen2.5's tokenizer, the start token ids of the Assistant (<|im_start|>assistant)

        if mode == "pre-train":
            packed_data = np.load(data_dir)
            self.all_input_ids = torch.tensor(packed_data["all_packed_input_ids"], dtype=torch.int32)
            self.all_attention_mask = torch.tensor(packed_data["all_packed_attention_masks"], dtype=torch.int32)
            self.all_labels = torch.tensor(packed_data["all_packed_labels"], dtype=torch.int32)
            del packed_data
        elif mode == "sft":
            dataset = json.load(open(data_dir))
            sequences = [tokenizer.apply_chat_template([
                {"role": "user", "content": data["input_seq"]},
                {"role": "assistant", "content": data["output_seq"]}
            ], add_generation_prompt = False, tokenize = False) for data in tqdm(dataset)]

            tokenized_results = tokenizer.batch_encode_plus(
                sequences,
                truncation = False
            )

            self.all_input_ids = []
            self.all_attention_mask = []
            self.all_labels = []
            
            num = 0
            for input_ids in tokenized_results["input_ids"]:
                if len(input_ids) > max_length: # pre-truncation
                    input_ids = input_ids[-max_length:]
                    num += 1
                self.all_input_ids.append(input_ids + [tokenizer.pad_token_id] * (max_length-len(input_ids)))
                self.all_attention_mask.append([1] * len(input_ids) + [0] * (max_length-len(input_ids)))
                # mask prompt loss
                self.all_labels.append(obtain_labels(input_ids, assistant_start_token_ids) + [-100] * (max_length-len(input_ids)))
                # no-mask prompt loss
                # self.all_labels.append(input_ids + [-100] * (max_length-len(input_ids)))
            print(f"There are {num} sequences have been truncated.")

            self.all_input_ids = torch.tensor(self.all_input_ids, dtype=torch.int64)
            self.all_attention_mask = torch.tensor(self.all_attention_mask, dtype=torch.int64)
            self.all_labels = torch.tensor(self.all_labels, dtype=torch.int64)

    def __getitem__(self, index):
        if self.mode == "pre-train":
            return {
                "input_ids": torch.tensor(self.all_input_ids[index], dtype=torch.int64),
                "attention_mask": torch.tensor(self.all_attention_mask[index], dtype=torch.int64),
                "labels": torch.tensor(self.all_labels[index], dtype=torch.int64)
            }
        elif self.mode == "sft":
            return {
                "input_ids": self.all_input_ids[index],
                "attention_mask": self.all_attention_mask[index],
                "labels": self.all_labels[index]
            }

    def __len__(self):
        return self.all_input_ids.shape[0]
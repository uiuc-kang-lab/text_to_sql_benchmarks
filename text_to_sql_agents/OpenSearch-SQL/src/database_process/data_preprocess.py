import argparse
import json
import os
import pickle
from pathlib import Path
import sqlite3
from tqdm import tqdm
import logging
# 设置基本配置
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
## 为dev train生成合适的文件，保存raw_question

def bird_pre_process(bird_dir,
                     with_evidence=False,
                     dev_json="dev/dev.json",
                     train_json="train_json",
                     dev_table="dev/dev_tables.json",
                     train_table="train/train_tables.json"):
    """
    Preprocesses bird-related data by loading JSON files, optionally appending evidence to questions,
    and saving the processed data into a specified directory.

    Args:
        bird_dir (str): The directory containing the bird data files.
        with_evidence (bool, optional): If True, appends evidence to the questions. Defaults to False.
        dev_json (str, optional): Path to the development JSON file. Defaults to "dev/dev.json".
        train_json (str, optional): Path to the training JSON file. Defaults to "train_json".
        dev_table (str, optional): Path to the development table JSON file. Defaults to "dev/dev_tables.json".
        train_table (str, optional): Path to the training table JSON file. Defaults to "train/train_tables.json".

    Returns:
        None: The function processes the data and saves it to the disk.
    """
    # ####修改
    # new_db_path = os.path.join(bird_dir, dev_database)
    # if not os.path.exists(new_db_path):
    #     os.system(f"mkdir -p {new_db_path}")
    #     os.system(f"cp -r {os.path.join(bird_dir, dev_database,'*')} {new_db_path}")
    # ####
    def json_preprocess(data_jsons):
        new_datas = []
        for data_json in data_jsons:
            ### Append the evidence to the question
            data_json["raw_question"]=data_json['question']
            if with_evidence and len(data_json["evidence"]) > 0:
                data_json['question'] = (data_json['question'] + " " + data_json["evidence"]).strip()
            new_datas.append(data_json)
        return new_datas
    
    preprocessed_path = Path(bird_dir) / "data_preprocess"
    preprocessed_path.mkdir(exist_ok=True)
    with open(os.path.join(bird_dir, dev_json)) as f:
        data_jsons = json.load(f)
        wf = open(os.path.join(preprocessed_path,'dev.json'), 'w')
        json.dump(json_preprocess(data_jsons), wf, indent=4)
    with open(os.path.join(bird_dir, train_json)) as f:
        data_jsons = json.load(f)
        wf = open(os.path.join(preprocessed_path,'train.json'), 'w')
        json.dump(json_preprocess(data_jsons), wf, indent=4)

    tables = []
    with open(os.path.join(bird_dir, dev_table)) as f:
        tables.extend(json.load(f))
    with open(os.path.join(bird_dir, train_table)) as f:
        tables.extend(json.load(f))
    with open(os.path.join(preprocessed_path,'tables.json'), 'w') as f:   #80 datas
        json.dump(tables, f, indent=4)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Process the Bird dataset.")
    parser.add_argument('--db_root_directory', type=str, help='Root directory for the database.')
    parser.add_argument('--dev_json', type=str, help='Path to the Dev JSON file.')
    parser.add_argument('--train_json', type=str, help='Path to the training JSON file.')
    parser.add_argument('--dev_table', type=str, help='Dev table name.')
    parser.add_argument('--train_table', type=str, help='Training table name.')

    args = parser.parse_args()
    logging.info(f"Start data_preprocess,the output_file is {args.db_root_directory}/data_preprocess")
    bird_pre_process(
        bird_dir=args.db_root_directory, 
        with_evidence=True, 
        dev_json=args.dev_json, 
        train_json=args.train_json, 
        dev_table=args.dev_table, 
        train_table=args.train_table
    )

import pickle
import gzip, re
import tqdm, json, random
import pandas as pd
import torch
import sqlite3, os
import numpy as np
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import euclidean_distances
import argparse
import logging
device = 'cuda:0' if torch.cuda.is_available() else 'cpu'
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

uuid_pattern = re.compile(
    r'^[0-9a-fA-F]{8}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{12}$'
)


def filter_column(table, col, exclude_num, num_shold=6000):
    cols=table[col].unique()
    if len(cols) > num_shold and exclude_num:
        try:
            table[col].dropna().astype(float)
            return []  # 跳过当前列，因为它满足排除条件
        except ValueError:
            pass
    # 排除具有UUID格式的数据
    col_vals = [
        item for item in cols if isinstance(item, str)
        and not uuid_pattern.match(item) and len(item) < 100
    ]
    return col_vals


def make_emb(db, DB_dir, DB_emb,col_values,bert_model,exclude_int=True):
    conn = sqlite3.connect(os.path.join(DB_dir, db, db + '.sqlite'))
    conn.text_factory = lambda x: str(x, 'utf-8', 'ignore')
    sql = "SELECT name FROM sqlite_master WHERE type='table';"
    df = pd.read_sql_query(sql, conn)
    print("db name:", db, "table count:", len(df.values))
    for table in df.values:
        table = table[0]
        if table[0] == 'sqlite_sequence':
                continue
        sql_t = f"SELECT * FROM '{table}';"
        values = pd.read_sql_query(sql_t, conn)
        values = values.select_dtypes(exclude=[np.number])
        for col in tqdm.tqdm(values.columns):
            col_vals = filter_column(values, col, exclude_int)###做索引的值：str
            if len(col_vals) == 0:
                continue
            train_embeddings = bert_model.encode(col_vals,device=device)##对值和embedding做相互索引
            DB_emb[table + "." + col] = train_embeddings
            col_values[table + "." + col] = col_vals


def save_emb(dicts, dbname, emb_dir):
    with gzip.open(os.path.join(emb_dir, f'{dbname}.pkl.gz'),
                   'wb') as pkl_file:
        pickle.dump(dicts, pkl_file, protocol=pickle.HIGHEST_PROTOCOL)


def load_emb(dbname, emb_dir="Bird/emb"):
    with gzip.open(os.path.join(emb_dir, f'{dbname}.pkl.gz'),
                   'rb') as pkl_file:
        data = pickle.load(pkl_file)
    with gzip.open(os.path.join(emb_dir, f'{dbname}_value.pkl.gz'),
                   'rb') as pkl_file:
        col_vs = pickle.load(pkl_file)

    return data, col_vs

def make_emb_all(data_dir, database, bertmodel):
    emb_dir=os.path.join(data_dir,"emb")
    os.makedirs(emb_dir, exist_ok=True)
    database=os.path.join(data_dir,database)
    data_dir=os.path.join(data_dir,"data_preprocess","dev.json")
    # init model
    bert_model = SentenceTransformer(bertmodel, device=device, cache_folder='model/')
    
    # load data
    Q = pd.read_json(data_dir)
    DB_dir = database
    DB_emb = {}
    Db_names = set()
    col_values = {}
    
    for i, (id, q) in enumerate(tqdm.tqdm(Q.iterrows())):
        db = q['db_id']
        if db not in Db_names:
            logging.info(f"Processing database: {db}") 
            col_values = {}
            DB_emb = {}
            make_emb(db, DB_dir, DB_emb, col_values,bert_model)
            save_emb(DB_emb, db, emb_dir)
            save_emb(col_values, db + '_value', emb_dir)
            Db_names.add(db)



if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Generate embeddings for the specified database.")
    parser.add_argument('--db_root_directory', type=str, help='Directory containing the data files.')
    parser.add_argument('--dev_database', type=str, help='Database file name.')
    parser.add_argument('--bert_model', type=str, help='Name of the BERT model to use.')

    args = parser.parse_args()
    logging.info(f"Start make_emb_for_dev,the output_file is {args.db_root_directory}/emb")
    make_emb_all(args.db_root_directory,args.dev_database,args.bert_model)

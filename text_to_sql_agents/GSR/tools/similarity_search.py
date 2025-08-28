import json
import math
import os
import sqlite3
from concurrent.futures import ThreadPoolExecutor

import faiss
import joblib
import numpy as np
from sklearn.decomposition import PCA
from tqdm import tqdm
from openai import OpenAI
from run.run_config import API_KEYS

client = OpenAI(
    api_key=API_KEYS)


def fetch_data_for_table_and_column(db_path, table_name, column):
    """
    Extracts data from specified tables and columns and generates text.
    :param db_path: SQLite Database Path
    :param table_name: table name
    :param column: column name
    :return: [{"id": row_id, "text": combined_text}, ...]
    """
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    selected_column = column

    # Queries the column information of the specified table
    cursor.execute(f"PRAGMA table_info(`{table_name}`)")
    columns_info = cursor.fetchall()

    exec_flag = False
    for current_column in columns_info:
        if current_column[1] == selected_column:
            if not current_column[5] > 0 and "TEXT" in current_column[2]:  # Check if it's not a primary key and type is TEXT
                exec_flag = True

    if any(keyword in selected_column.lower() for keyword in ["_id", " id", "url", "email", "web", "time", "phone", "date", "address"]) or selected_column.endswith("Id"):
        exec_flag = False

    try:
        cursor.execute(f"""
                        SELECT SUM(LENGTH(unique_values)), COUNT(unique_values)
                        FROM (
                            SELECT DISTINCT `{selected_column}` AS unique_values
                            FROM `{table_name}`
                            WHERE `{selected_column}` IS NOT NULL
                        ) AS subquery
                    """)
        nums_result = cursor.fetchone()
    except:
        nums_result = 0, 0

    sum_of_lengths, count_distinct = nums_result
    if sum_of_lengths is None or count_distinct == 0:
        exec_flag = False

    average_length = sum_of_lengths / count_distinct
    if not (("name" in selected_column.lower() and sum_of_lengths < 5000000) or (
            sum_of_lengths < 2000000 and average_length < 25) or count_distinct < 100):
        exec_flag = False

    if exec_flag:
        try:
            query = f"SELECT DISTINCT `{selected_column}` FROM `{table_name}` WHERE `{selected_column}` IS NOT NULL"
            cursor.execute(query)
            rows = cursor.fetchall()
            conn.close()

            processed_data = [{"raw_data": str(row[0])} for row in rows]

            return processed_data, exec_flag
        except Exception as e:
            conn.close()
            exec_flag = False
            return [], exec_flag
    else:
        conn.close()
        return [], exec_flag


def reduce_dimension(embeddings, target_dim=512, save_pca_model = False, pca_model_file = None):
    """
    Dimensionality reduction of embedding vectors using PCA
    :param embeddings: Raw embedding vector (numpy array)
    :param target_dim: Target dimension after dimensionality reduction
    :return: Embedding vector after dimensionality reduction
    """
    n_samples, n_features = embeddings.shape
    adjusted_dim = min(target_dim, n_samples, n_features)  # Dynamic adjustment of target dimensions
    pca = PCA(n_components=adjusted_dim)
    reduced_embeddings = pca.fit_transform(embeddings)

    if save_pca_model and pca_model_file:
        joblib.dump(pca, pca_model_file)
    return reduced_embeddings


def generate_embeddings(batch_data, model="text-embedding-3-small"):
    """Generate embedding vectors"""
    try:
        response = client.embeddings.create(input=batch_data, model=model)
        return [result.embedding for result in response.data]
    except Exception as e:
        raise


def process_batches(raw_data_list, initial_batch_size=2000, model="text-embedding-3-small", index=None, target_dim=512, pca_model_file=None):
    """Batch process data, generate embedding and write to Faiss indexes in real time"""
    batch_size = initial_batch_size
    i = 0
    if model == 'text-embedding-3-small':
        emb_dimension = 1536
    elif model == 'text-embedding-3-large':
        emb_dimension = 3072
    process_ready_embeddings_batch = np.empty((0, emb_dimension), dtype='float32')
    skip_embedding_flag = False
    with tqdm(total=len(raw_data_list), desc="Processing batches", unit="record") as pbar:
        while i < len(raw_data_list):
            batch_data = raw_data_list[i:i + batch_size]
            while True:
                if not skip_embedding_flag:     # No skip coding
                    try:
                        embeddings_batch = generate_embeddings(batch_data, model)
                        embeddings_batch = np.array(embeddings_batch).astype('float32')

                        i += len(batch_data)
                        # batch_size = initial_batch_size   # Callback batch_size to initial_batch_size

                        # Use np.concatenate() to splice the batch embedding
                        process_ready_embeddings_batch = np.concatenate([process_ready_embeddings_batch, embeddings_batch], axis=0)

                    except Exception as e:
                        if batch_size == 1:     # If batch_size is equal to 1, neither can be encoded, then skip this data
                            i += len(batch_data)
                            if i != len(raw_data_list):     # Not the last one.
                                batch_size = initial_batch_size // 4  # Callback batch_size to a smaller initial_batch_size
                                batch_data = raw_data_list[i:i + batch_size]
                                continue
                            else:       # It's the last data.
                                skip_embedding_flag = True
                                continue

                        batch_size = len(batch_data)
                        batch_size = max(batch_size // 2, 1)  # Make sure batch_size is at least 1
                        batch_data = raw_data_list[i:i + batch_size]  # Adjusting the current batch size
                        continue  # Continue trying to process the current batch

                if len(raw_data_list) - i <= target_dim and len(raw_data_list) != i:
                    batch_data = raw_data_list[i:]
                    continue

                if process_ready_embeddings_batch.shape[0] >= 3 * initial_batch_size or len(raw_data_list) == i:
                    if process_ready_embeddings_batch.shape[0] > 0:
                        # PCA downgrading
                        reduced_embeddings_batch = reduce_dimension(process_ready_embeddings_batch, target_dim, save_pca_model=True, pca_model_file=pca_model_file)
                        # Add the generated embedding to the Faiss index in real time
                        index.add(reduced_embeddings_batch)
                        pbar.update(len(reduced_embeddings_batch))  # Update progress bar
                        process_ready_embeddings_batch = np.empty((0, emb_dimension), dtype='float32')  # Reset to handle embedded arrays
                    break
                else:
                    batch_data = raw_data_list[i:i + batch_size]
                    continue

    return index

def parallel_process_batches(raw_data_list, initial_batch_size=2000, model="text-embedding-3-small", target_dim=512, num_workers=4, pca_model_file=None):
    """
    Parallel processing of data, generating embeddings and writing to Faiss indexes in real time, with dimensionality reduction
    :param raw_data_list: Raw data list
    :param initial_batch_size: Batch size
    :param model: Embedding Generative Models
    :param target_dim: Target dimension after dimensionality reduction
    :param num_workers: Number of threads/processes working in parallel
    :return: Consolidated Faiss index
    """
    def split_data(data, num_splits):
        chunk_size = math.ceil(len(data) / num_splits)
        return [data[i:i + chunk_size] for i in range(0, len(data), chunk_size)]

    data_chunks = split_data(raw_data_list, num_workers)

    # Initialising Faiss Indexes
    dimension = target_dim
    master_index = faiss.IndexFlatL2(dimension)

    # perform parallel tasks
    def process_chunk(chunk):
        local_index = faiss.IndexFlatL2(dimension)
        local_index = process_batches(chunk, initial_batch_size, model, local_index, target_dim, pca_model_file)
        return local_index

    with ThreadPoolExecutor(max_workers=num_workers) as executor:
        futures = [executor.submit(process_chunk, chunk) for chunk in data_chunks]
        for future in futures:
            local_index = future.result()
            master_index.merge_from(local_index)  # Merging Sub-Indexes to the Main Index

    return master_index


def save_metadata(raw_data_list, metadata_file="metadata.json"):
    """Save metadata to file"""
    metadata = {str(i): raw_data_list[i] for i in range(len(raw_data_list))}
    with open(metadata_file, "w") as f:
        json.dump(metadata, f)
    return metadata  # Returns metadata for use in queries


def query_faiss_index_with_pca(index, query_embedding, pca_model_file, top_k=5):
    pca = joblib.load(pca_model_file)  # Loading PCA Models
    query_embedding_reduced = pca.transform(np.array([query_embedding]).astype('float32'))
    """Querying the Faiss Index"""
    distances, indices = index.search(query_embedding_reduced, top_k)
    return distances, indices

def research(db_path, table_name, column, keyword):

    embedding_model = 'text-embedding-3-small'
    database_name = db_path.split("/")[-2]
    vector_directory = f"../data/vector_data/{database_name}/{table_name}/{column}"

    if not os.path.exists(vector_directory):
        os.makedirs(vector_directory)
        #print(f"The directory {vector_directory} has been created.")

    base_name = vector_directory + f"/{table_name}_{column}"
    index_file = f"{base_name}_faiss_index.bin"
    metadata_file = f"{base_name}_metadata.json"
    pca_model_file = f"{base_name}_pca_model.pkl"

    # If both the index file and the metadata file exist, they are loaded and queried directly
    if os.path.exists(index_file) and os.path.exists(metadata_file) and os.path.exists(pca_model_file):
        #print("Loading pre-stored indexes and metadata...")
        #print(index_file)
        index = faiss.read_index(index_file)
        with open(metadata_file, "r") as f:
            metadata = json.load(f)
    else:
        # If the file does not exist, generate the index and embedding
        #print("Index or metadata file not found, start generating embedding and indexing...")
        # Getting data for a specified table and column
        data, exec_flag = fetch_data_for_table_and_column(db_path, table_name, column)

        if not exec_flag:
            #print("This column does not need to store")
            output_sample = []
            return output_sample

        # Extract raw_data for all records
        raw_data_list = [record["raw_data"] for record in data]

        if '' in raw_data_list:
            #print(f"Empty characters in the data of {table_name}'s {column}.")
            raw_data_list = [item for item in raw_data_list if item.strip()]

        initial_batch_size = 2000
        num_workers = 8
        dimension = 512
        embeddings = []

        if len(raw_data_list) < num_workers * initial_batch_size:
            if len(raw_data_list) < dimension:
                dimension = len(raw_data_list)
            index = faiss.IndexFlatL2(dimension)
            index = process_batches(raw_data_list, initial_batch_size, model=embedding_model, index=index,
                                    target_dim=dimension, pca_model_file=pca_model_file)
        else:
            # Batch process data and generate embeds
            index = parallel_process_batches(raw_data_list, initial_batch_size, model=embedding_model,
                                             target_dim=dimension, num_workers=num_workers, pca_model_file=pca_model_file)

        # Save Faiss Index
        faiss.write_index(index, index_file)

        # Save the metadata and return
        metadata = save_metadata(raw_data_list, metadata_file)

    # query
    response = client.embeddings.create(input=keyword, model=embedding_model)
    query_embedding = np.array(response.data[0].embedding).astype('float32')

    top_k = 5
    distances, indices = query_faiss_index_with_pca(index, query_embedding, pca_model_file, top_k)
    output_sample = [metadata[str(idx)] for idx in indices[0]]

    return output_sample

import argparse
import concurrent.futures
import json
import multiprocessing
import os
import time
from concurrent.futures import ProcessPoolExecutor
from dataclasses import dataclass
from typing import Any, Dict, List, Tuple

import numpy as np
import spacy
from dotenv import load_dotenv
from tqdm import tqdm

from text2sql.data import SchemaManager, SqliteDataset
from text2sql.data.query_parser import get_table_mapping
from text2sql.engine.embeddings import BedrockCohereEmbedder, EmbeddingResult


@dataclass
class ProcessingResult:
    """Result of processing a single query."""

    item: Dict[str, Any]
    is_valid: bool
    is_invalid: bool
    is_single_table: bool


@dataclass
class TimingStats:
    """Timing statistics for query processing."""

    schema_lookup: float = 0.0
    table_mapping: float = 0.0
    schema_filtering: float = 0.0
    query_validation: float = 0.0
    ner_extraction: float = 0.0
    total: float = 0.0


def parse_arguments():
    """
    Parse command line arguments.

    Returns:
        Parsed arguments
    """
    parser = argparse.ArgumentParser(description="Process SQL queries and prepare training data.")

    parser.add_argument(
        "--train-databases-path",
        type=str,
        required=True,
        help="Path to the training databases directory",
    )

    parser.add_argument(
        "--train-data-path",
        type=str,
        required=True,
        help="Path to the training data JSON file",
    )

    parser.add_argument(
        "--tables-json-path",
        type=str,
        required=True,
        help="Path to the tables JSON file",
    )

    parser.add_argument(
        "--output-path",
        type=str,
        required=True,
        help="Path to save the output JSON file",
    )

    parser.add_argument("--subset", type=int, default=0, help="Number of samples to process (0 for all)")

    parser.add_argument(
        "--max-processes",
        type=int,
        default=8,
        help="Maximum number of processes to use",
    )

    return parser.parse_args()


def load_data(
    train_databases_path: str, train_data_path: str, subset: int = 0
) -> Tuple[SqliteDataset, List[Dict[str, Any]]]:
    """
    Load training data and initialize dataset.

    Returns:
        Tuple containing the SQLiteDataset and the training data
    """
    sql_dataset = SqliteDataset(train_databases_path)
    with open(train_data_path, "r") as f:
        train_data = json.load(f)
        if subset:
            train_data = train_data[:subset]
    return sql_dataset, train_data


def get_filtered_schema_txt(
    table_map: Dict[str, Any],
    db_id: str,
    schema_manager: SchemaManager,
) -> Dict[str, str]:
    """
    Get filtered schema text in different formats.

    Args:
        sql_dataset: The SQLiteDataset instance
        table_map: Mapping of tables to keep
        db_id: Database ID
        schema_manager: SchemaManager instance

    Returns:
        Dictionary containing schema text in different formats
    """

    sql_create_text = schema_manager.get_filtered_schema(db_id, table_map, "sql")
    m_schema_text = schema_manager.get_filtered_schema(db_id, table_map, "m_schema")
    mac_schema_text = schema_manager.get_filtered_schema(db_id, table_map, "mac_schema")

    return {
        "sql": sql_create_text,
        "m_schema": m_schema_text,
        "mac_schema": mac_schema_text,
    }


def extract_named_entities(text):
    """
    Extract named entities from text using spaCy
    """
    # Load spaCy model - you can choose different models based on your needs
    # en_core_web_sm is smaller/faster, en_core_web_lg is more accurate but larger
    nlp = spacy.load("en_core_web_sm")

    # Process the text
    doc = nlp(text)

    # Extract named entities
    named_entities = {}
    for entity in doc.ents:
        entity_type = entity.label_
        entity_text = entity.text

        # Initialize the list for this entity type if it doesn't exist
        if entity_type not in named_entities:
            named_entities[entity_type] = []

        # Add this entity to the list
        named_entities[entity_type].append(entity_text)

    return named_entities


def replace_entities_with_tokens(question, named_entities):
    """
    Replace named entities with special tokens based on their type
    If entity is not a named entity but matches enumeration values, replace with column name
    """
    skeleton_question = question

    # Replace named entities with special tokens
    for entity_type, entities in named_entities.items():
        for entity in entities:
            # Use <TYPE> format for entity replacement
            skeleton_question = skeleton_question.replace(entity, f"<{entity_type.lower()}>")

    return skeleton_question


def process_single_query(
    item: Dict[str, Any], sql_dataset: SqliteDataset, schema_manager: SchemaManager
) -> ProcessingResult:
    """
    Process a single query and return its validation status.

    Args:
        item: Query item to process
        sql_dataset: SQLiteDataset instance
        schema_manager: SchemaManager instance

    Returns:
        ProcessingResult containing the processed item and status flags
    """
    # Create a copy to avoid modifying the original
    item = item.copy()
    timing = TimingStats()
    t0 = time.time()

    try:
        # Get schema info for this database
        t0_schema = time.time()
        schema_info = sql_dataset.get_database_schema(item["db_id"])
        timing.schema_lookup = time.time() - t0_schema

        # Get table mapping for this query
        t1_mapping = time.time()
        table_mapping = get_table_mapping(schema_info, item["SQL"])
        timing.table_mapping = time.time() - t1_mapping

        # Get filtered schema
        t2_filter = time.time()
        filtered_schema_dict = get_filtered_schema_txt(table_mapping["table_map"], item["db_id"], schema_manager)
        timing.schema_filtering = time.time() - t2_filter

        item.update(filtered_schema_dict)

        # Update table count in train data
        item["table_count"] = len(table_mapping["tables"])

        # If query uses more than one table, validate and execute it
        if len(table_mapping["tables"]) > 1:
            t3_validation = time.time()
            result = sql_dataset.validate_query(item["db_id"], item["SQL"], timeout_secs=5)
            timing.query_validation = time.time() - t3_validation

            if result["validated"] or result["message"].startswith("query timed out"):
                t4_ner = time.time()
                entities = extract_named_entities(item["question"])
                item["question_masked"] = replace_entities_with_tokens(item["question"], entities)
                timing.ner_extraction = time.time() - t4_ner

                timing.total = time.time() - t0
                item["timing"] = timing.__dict__
                return ProcessingResult(item, True, False, False)

            timing.total = time.time() - t0
            item["timing"] = timing.__dict__
            return ProcessingResult(item, False, True, False)

        timing.total = time.time() - t0
        item["timing"] = timing.__dict__
        return ProcessingResult(item, False, False, True)

    except Exception as e:
        print(f"Error processing query for db {item['db_id']}: {str(e)}")
        timing.total = time.time() - t0
        item["timing"] = timing.__dict__
        return ProcessingResult(item, False, True, False)


def save_results(valid_multi_table_queries: List[Dict[str, Any]], output_path: str) -> None:
    """
    Save the processed results to files.

    Args:
        valid_multi_table_queries: List of valid multi-table queries
        train_data: Training data
    """
    # Remove timing information before saving
    for item in valid_multi_table_queries:
        if "timing" in item:
            del item["timing"]

    with open(output_path, "w") as f:
        json.dump(valid_multi_table_queries, f, indent=2, ensure_ascii=False)


def print_statistics(
    train_data: List[Dict[str, Any]],
    valid_multi_table_queries: List[Dict[str, Any]],
    single_table_count: int,
    invalid_query_count: int,
) -> None:
    """
    Print processing statistics.

    Args:
        train_data: Original training data
        valid_multi_table_queries: Valid multi-table queries
        single_table_count: Count of single-table queries
        invalid_query_count: Count of invalid queries
    """
    print(f"Original queries: {len(train_data)}")
    print(f"Valid multi-table queries: {len(valid_multi_table_queries)}")
    print(f"Single-table queries removed: {single_table_count}")
    print(f"Invalid queries removed: {invalid_query_count}")
    print(f"Total queries removed: {len(train_data) - len(valid_multi_table_queries)}")


def process_chunk(
    chunk: List[Dict[str, Any]],
    sql_dataset: SqliteDataset,
    schema_manager: SchemaManager,
) -> List[ProcessingResult]:
    """
    Process a chunk of queries in a single process.

    Args:
        chunk: List of query items to process
        sql_dataset: SQLiteDataset instance
        schema_manager: SchemaManager instance

    Returns:
        List of ProcessingResults
    """
    results = []
    for item in chunk:
        result = process_single_query(item, sql_dataset, schema_manager)
        results.append(result)
    return results


def process_queries(args) -> None:
    """Main function to process and filter queries using ProcessPoolExecutor."""
    # Initialize and load data
    t_start = time.time()
    sql_dataset, train_data = load_data(args.train_databases_path, args.train_data_path, args.subset)

    print("Initializing schema manager")
    schema_manager = SchemaManager(sql_dataset, table_descriptions_path=args.tables_json_path)
    print("Schema manager initialized")

    init_time = time.time() - t_start
    print(f"Initialization time: {init_time:.2f} seconds")

    # Determine number of processes to use
    num_processes = min(multiprocessing.cpu_count(), args.max_processes)
    print(f"Using {num_processes} processes for parallel processing")

    # Divide data into chunks for each process
    chunk_size = (len(train_data) + num_processes - 1) // num_processes
    chunks = [train_data[i : i + chunk_size] for i in range(0, len(train_data), chunk_size)]

    # Create a progress bar
    total_items = len(train_data)
    progress_bar = tqdm(total=total_items, desc="Processing queries")

    # Process each chunk in its own process
    all_results = []
    with ProcessPoolExecutor(max_workers=num_processes) as executor:
        # Submit all tasks
        future_to_chunk = {
            executor.submit(process_chunk, chunk, sql_dataset, schema_manager): len(chunk) for chunk in chunks
        }

        # As each task completes, update the progress bar
        for future in concurrent.futures.as_completed(future_to_chunk):
            chunk_size = future_to_chunk[future]
            try:
                results = future.result()
                all_results.extend(results)
                progress_bar.update(chunk_size)
            except Exception as exc:
                print(f"A chunk generated an exception: {exc}")
                progress_bar.update(chunk_size)

    # Close the progress bar
    progress_bar.close()

    # Process results
    valid_multi_table_queries = []
    single_table_count = 0
    invalid_query_count = 0
    total_timing = TimingStats()

    for result in all_results:
        # Accumulate timing information
        for key, value in result.item["timing"].items():
            setattr(total_timing, key, getattr(total_timing, key) + value)

        if result.is_valid:
            valid_multi_table_queries.append(result.item)
        elif result.is_invalid:
            invalid_query_count += 1
        elif result.is_single_table:
            single_table_count += 1

    # Print timing statistics
    total_time = time.time() - t_start
    print(f"\nTotal execution time: {total_time:.2f} seconds")

    print("\nTiming Statistics (averages per query):")
    print("Total queries processed:", len(train_data))
    for key, value in total_timing.__dict__.items():
        avg_time = value / len(train_data)
        print(f"{key}: {avg_time:.3f} seconds")

    # Save results and print statistics
    save_results(valid_multi_table_queries, args.output_path)
    print_statistics(train_data, valid_multi_table_queries, single_table_count, invalid_query_count)

    # Get the embeddings
    load_dotenv()

    embedder = BedrockCohereEmbedder(
        model=os.getenv("AWS_MODEL_NAME"),
        region_name=os.getenv("AWS_REGION_NAME"),
        input_type=os.getenv("AWS_INPUT_TYPE"),
    )

    embedding_path = args.output_path.replace(".json", "_embeddings.npy")
    print(f"generating train embeddings and saving to '{embedding_path}'")
    masked_questions = [item["question_masked"] for item in valid_multi_table_queries]
    train_embedding_response: EmbeddingResult = embedder.embed(masked_questions, verbose=True)
    train_embeddings = train_embedding_response.embedding
    assert len(train_embeddings) == len(masked_questions)
    np.save(embedding_path, train_embeddings)


if __name__ == "__main__":
    multiprocessing.freeze_support()  # For Windows compatibility

    # Parse command line arguments
    args = parse_arguments()

    # Run the main processing function
    process_queries(args)

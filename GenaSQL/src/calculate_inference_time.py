import argparse
import json
import os

from typing import Annotated, Literal

import pandas as pd

from dotenv import load_dotenv
from loguru import logger
from pydantic import AfterValidator, BaseModel

from text2sql.data.datasets import SCHEMA_FORMATS
from text2sql.engine.embeddings import EmbeddingResult
from text2sql.engine.generation import GenerationResult


def verify_schema_format(schema_format: str):
    if schema_format not in SCHEMA_FORMATS:
        raise ValueError(f"Invalid schema format: {schema_format}")
    return schema_format


class SchemaLinkingInfo(BaseModel):
    question_id: int
    model_name: str
    schema_format: Annotated[str, AfterValidator(verify_schema_format)]
    messages: list[dict]
    generator_output: GenerationResult
    prediction: str
    table_linking: dict | None
    column_linking: dict | None
    table_description: str
    column_description: str
    full_description: str


class RewriteInfo(BaseModel):
    question_id: int
    original_sql: str
    rewritten_sql: str
    is_rewritten: bool  # whether the candidate was rewritten successfully (even if rewritten sql is same)
    messages: list[dict]
    generator_output: GenerationResult | None


class Candidate(BaseModel):
    question_id: int
    config_index: int
    sample: dict
    schema_format: Annotated[str, AfterValidator(verify_schema_format)]
    schema_filtering: Literal["none", "table", "column"]
    messages: list[dict]
    generator_output: GenerationResult
    original_sql: str  # first generation parsed result
    candidate_sql: str  # final candidate sql after rewrite
    rewrite_checked: bool = False
    rewrite_info: list[RewriteInfo] = []


class CandidateList(BaseModel):
    question_id: int
    candidate_configs: list[dict]
    candidates: list[Candidate]


class CandidateSelection(BaseModel):
    question_id: int
    db_id: str  # for formatting output
    generator_outputs: list[GenerationResult] = []
    candidate_config: dict
    selected_idx: int
    selected_sql: str


class InferenceTimeInfo(BaseModel):
    question_id: int | None = None
    schema_linking_ms: int | None = None
    embedding_ms: int | None = None
    sql_generation_ms: int | None = None
    sql_rewrite_ms: int | None = None
    sql_rewrite_max_count: int | None = None
    sql_rewrite_ttl_count: int | None = None
    chase_selection_ms: int | None = None
    chase_selection_ttl_count: int | None = None
    total_ms: int | None = None


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--test-json-path",
        type=str,
        required=True,
        help="path to the test.json file",
    )
    parser.add_argument(
        "--output-path",
        type=str,
        required=True,
        default="../outputs",
        help="target output path",
    )
    args = parser.parse_args()

    load_dotenv()

    # load test.json
    logger.info("Loading test data...")
    with open(args.test_json_path, "r") as f:
        test_data: list[dict] = json.load(f)
    logger.info(f"Loaded {len(test_data)} test samples")

    #############################
    # preprocessing
    #############################
    test_question_ids = [sample["question_id"] for sample in test_data]

    #############################
    # schema linking
    # outputs: list[SchemaLinkingOutput]
    #############################
    # load any existing schema linking jsons
    schema_linking_output_dir = os.path.join(args.output_path, "1_schema_linking")
    os.makedirs(schema_linking_output_dir, exist_ok=True)

    schema_linking_results: dict = {}
    for file in sorted(os.listdir(schema_linking_output_dir)):
        if file.startswith("schema-linking_") and file.endswith(".json"):
            # get question id from filename
            question_id = int(file.rsplit(".", 1)[0].rsplit("-", 1)[-1])
            if question_id in test_question_ids:
                with open(os.path.join(schema_linking_output_dir, file), "r") as f:
                    schema_linking_output: SchemaLinkingInfo = SchemaLinkingInfo.model_validate_json(f.read())
                    model_name = schema_linking_output.model_name
                    schema_format = schema_linking_output.schema_format
                    if question_id not in schema_linking_results:
                        schema_linking_results[question_id] = {}
                    if model_name not in schema_linking_results[question_id]:
                        schema_linking_results[question_id][model_name] = {}
                    schema_linking_results[question_id][model_name][schema_format] = schema_linking_output
    # for verification, all question ids should be in schema_linking_results
    logger.info(f"Loaded {len(schema_linking_results)} cached schema linking results")
    missing_question_ids = set([s["question_id"] for s in test_data if s["question_id"] not in schema_linking_results])
    if missing_question_ids:
        logger.error(f"Missing schema linking results for question IDs: {sorted(list(missing_question_ids))}")
        raise ValueError(f"Missing schema linking results for {len(missing_question_ids)} questions")

    #############################
    # question embedding
    # outputs: EmbeddingResult
    #############################
    embedding_output_dir = os.path.join(args.output_path, "2_embeddings")
    os.makedirs(embedding_output_dir, exist_ok=True)
    embedding_results: dict[int, EmbeddingResult] = {}
    for file in os.listdir(embedding_output_dir):
        if os.path.basename(file).startswith("embedding_qid-") and file.endswith(".json"):
            # get id from filename
            question_id = int(file.rsplit(".", 1)[0].rsplit("-", 1)[-1])
            if question_id in test_question_ids:
                with open(os.path.join(embedding_output_dir, file), "r") as f:
                    embedding_results[question_id] = EmbeddingResult.model_validate_json(f.read())
    # for verification, all question ids should be in embedding_results
    logger.info(f"Loaded {len(embedding_results)} cached embedding results")
    missing_samples = [sample for sample in test_data if sample["question_id"] not in embedding_results]
    if missing_samples:
        missing_ids = [s["question_id"] for s in missing_samples]
        logger.error(f"Missing embedding results for question IDs: {sorted(missing_ids)}")
        raise ValueError(f"Missing embedding results for {len(missing_samples)} questions")

    #############################
    # sql candidate generation
    #############################
    sql_generation_output_dir = os.path.join(args.output_path, "4_candidate_generation")
    os.makedirs(sql_generation_output_dir, exist_ok=True)

    sql_candidate_lists: dict[int, list[Candidate]] = {}
    for file in os.listdir(sql_generation_output_dir):
        if os.path.basename(file).startswith("candidates_qid-") and file.endswith(".json"):
            question_id = int(file.rsplit(".", 1)[0].rsplit("-", 1)[-1])
            if question_id in test_question_ids:
                with open(os.path.join(sql_generation_output_dir, file), "r") as f:
                    bundle = CandidateList.model_validate_json(f.read())
                    sql_candidate_lists[question_id] = bundle.candidates
    # for verification, all question ids should be in sql_candidate_lists
    logger.info(f"Loaded {len(sql_candidate_lists)} cached SQL candidate lists")
    missing_samples = [sample for sample in test_data if sample["question_id"] not in sql_candidate_lists]
    if missing_samples:
        missing_ids = [s["question_id"] for s in missing_samples]
        logger.error(f"Missing SQL candidate lists for question IDs: {sorted(missing_ids)}")
        raise ValueError(f"Missing SQL candidate lists for {len(missing_samples)} questions")

    #############################
    # candidate selection
    #############################
    candidate_selection_output_dir = os.path.join(args.output_path, "5_candidate_selection")
    os.makedirs(candidate_selection_output_dir, exist_ok=True)

    candidate_selections: dict[int, CandidateSelection] = {}
    for file in os.listdir(candidate_selection_output_dir):
        if os.path.basename(file).startswith("selection_qid-") and file.endswith(".json"):
            question_id = int(file.rsplit(".", 1)[0].rsplit("-", 1)[-1])
            if question_id in test_question_ids:
                with open(os.path.join(candidate_selection_output_dir, file), "r") as f:
                    candidate_selections[question_id] = CandidateSelection.model_validate_json(f.read())
    logger.info(f"Loaded {len(candidate_selections)} cached candidate selection results")
    missing_samples = [s for s in test_data if s["question_id"] not in candidate_selections]
    if missing_samples:
        missing_ids = [s["question_id"] for s in missing_samples]
        logger.error(f"Missing selection info for question IDs: {sorted(missing_ids)}")
        raise ValueError(f"Missing selection info for {len(missing_samples)} questions")

    #############################
    # inference time
    #############################
    inference_time_info: list[InferenceTimeInfo] = []
    for question_id in test_question_ids:
        # Initialize inference time info for this question
        info = InferenceTimeInfo(question_id=question_id)

        # Calculate schema linking time - get max time over all models and schema formats
        schema_linking_times: list[int] = []
        for model_name in schema_linking_results[question_id]:
            for schema_format in schema_linking_results[question_id][model_name]:
                schema_linking_info: SchemaLinkingInfo = schema_linking_results[question_id][model_name][schema_format]
                if schema_linking_info.generator_output and schema_linking_info.generator_output.tokens:
                    schema_linking_times.append(schema_linking_info.generator_output.tokens.inf_time_ms)

        if schema_linking_times:
            info.schema_linking_ms = max(schema_linking_times)

        # Calculate embedding time
        if question_id in embedding_results:
            info.embedding_ms = embedding_results[question_id].inf_time_ms

        # Calculate SQL generation and rewrite time
        if question_id in sql_candidate_lists:
            candidates: list[Candidate] = sql_candidate_lists[question_id]

            # Get max generation time across all candidates
            generation_times: list[int] = []
            for candidate in candidates:
                if candidate.generator_output and candidate.generator_output.tokens:
                    generation_times.append(candidate.generator_output.tokens.inf_time_ms)

            if generation_times:
                info.sql_generation_ms = max(generation_times)

            # Calculate rewrite time - sum all rewrites for each candidate and take the max total
            rewrite_times: list[int] = []
            rewrite_counts: list[int] = []
            for candidate in candidates:
                if candidate.rewrite_info:
                    candidate_rewrite_time: int = 0
                    for rewrite in candidate.rewrite_info:
                        if rewrite.generator_output and rewrite.generator_output.tokens:
                            candidate_rewrite_time += rewrite.generator_output.tokens.inf_time_ms
                    rewrite_times.append(candidate_rewrite_time)
                    rewrite_counts.append(len(candidate.rewrite_info))
            if rewrite_times:
                info.sql_rewrite_ms = max(rewrite_times)
                info.sql_rewrite_max_count = max(rewrite_counts)
                info.sql_rewrite_ttl_count = sum(rewrite_counts)

        # Calculate candidate selection time
        selection_count: int = 0
        if question_id in candidate_selections:
            selection: CandidateSelection = candidate_selections[question_id]
            if selection.generator_outputs:
                selection_times: list[int] = []
                for output in selection.generator_outputs:
                    if output.tokens:
                        selection_times.append(output.tokens.inf_time_ms)
                        selection_count += 1
                if selection_times:
                    info.chase_selection_ms = max(selection_times)
            info.chase_selection_ttl_count = selection_count

        # calculate total time. exclude None values
        total_time = 0
        for step_time in [
            info.schema_linking_ms,
            info.embedding_ms,
            info.sql_generation_ms,
            info.sql_rewrite_ms,
            info.chase_selection_ms,
        ]:
            if step_time:
                total_time += step_time

        info.total_ms = total_time

        # "soft" checks
        if info.schema_linking_ms is None:
            logger.warning(f"Schema linking time is None for question ID: {question_id}")
        if info.embedding_ms is None:
            logger.warning(f"Embedding time is None for question ID: {question_id}")
        if info.sql_generation_ms is None:
            logger.warning(f"SQL generation time is None for question ID: {question_id}")

        inference_time_info.append(info)

    #############################
    # output saving
    #############################

    # Save as CSV using pandas
    df = pd.DataFrame([info.model_dump() for info in inference_time_info])

    # Fill None values with 0 for time columns
    time_columns = [col for col in df.columns if col != "question_id"]
    df[time_columns] = df[time_columns].fillna(0)

    # Save to CSV
    output_csv_path = os.path.join(args.output_path, "inference_times.csv")
    df.to_csv(output_csv_path, index=False)
    logger.info(f"Saved inference times to {output_csv_path}")

    # calculate min, first quartile, median, third quartile, max, std dev and mean for each time
    time_statistics: list[dict] = []
    for column in df.columns:
        if column in ["question_id"]:
            continue
        time_statistics.append(
            {
                "step": column,
                "min": df[column].min(),
                "first_quartile": df[column].quantile(0.25),
                "median": df[column].median(),
                "third_quartile": df[column].quantile(0.75),
                "max": df[column].max(),
                "std_dev": df[column].std(),
                "mean": df[column].mean(),
            }
        )
    # save to csv
    time_statistics_csv_path = os.path.join(args.output_path, "inference_times_statistics.csv")
    pd.DataFrame(time_statistics).to_csv(time_statistics_csv_path, index=False)
    logger.info(f"Saved inference times statistics to {time_statistics_csv_path}")


if __name__ == "__main__":
    main()

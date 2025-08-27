#!/usr/bin/env python
import argparse
import json
import os
from typing import Dict, List, Any

import tqdm

from loguru import logger

from text2sql.data.datasets import SqliteDataset
from text2sql.evaluation.metrics.execution_match import execution_match


def main():
    parser = argparse.ArgumentParser(description="Calculate execution match score for SQL predictions")
    parser.add_argument(
        "--test-database-path",
        type=str,
        required=True,
        help="Path to the test databases base directory",
    )
    parser.add_argument(
        "--test-json-path",
        type=str,
        required=True,
        help="Path to the test.json file containing ground truth data",
    )
    parser.add_argument(
        "--predictions-path",
        type=str,
        required=True,
        help="Path to the predictions.json file containing model predictions",
    )
    args = parser.parse_args()

    # Create SQLiteDataset
    dataset = SqliteDataset(args.test_database_path)

    # Load test data
    with open(args.test_json_path, "r") as f:
        test_data = json.load(f)

    # Load predictions
    with open(args.predictions_path, "r") as f:
        predictions = json.load(f)

    # Create a mapping from question_id to test data for easier lookup
    test_data_map = {str(item["question_id"]): item for item in test_data}

    # Initialize result list
    results: list[int] = []
    valid_count: int = 0
    # Process each prediction
    for question_id, predicted_sql in tqdm.tqdm(predictions.items(), desc="Evaluating predictions"):
        # Skip if the question_id is not in the test data
        if question_id not in test_data_map:
            print(f"Warning: Question ID {question_id} not found in test data, skipping")
            continue

        test_item = test_data_map[question_id]
        db_id = test_item["db_id"]
        ground_truth_sql = test_item["SQL"]

        try:
            # Execute predicted SQL
            predicted_result_dict = dataset.validate_query(db_id, predicted_sql)
            prediction_valid = predicted_result_dict.get("validated", False)
            predicted_results = predicted_result_dict.get("execution_result", [])

            # Execute ground truth SQL
            ground_truth_result_dict = dataset.validate_query(db_id, ground_truth_sql)
            ground_truth_results = ground_truth_result_dict.get("execution_result", [])

            # Compare results
            is_match = prediction_valid and execution_match(predicted_results, ground_truth_results)

            if prediction_valid:
                valid_count += 1

            results.append(int(is_match))

        except Exception as e:
            # print(f"Error processing question ID {question_id}: {str(e)}")
            results.append(0)

    # Calculate and print average score
    if len(results) > 0:
        average_score = sum(results) / len(results)
        valid_percentage = valid_count / len(results)
        print()
        print(f"Valid Percentage : {valid_percentage:.4f} ({valid_count}/{len(results)})")
        print(f"Execution Match  : {average_score:.4f} ({sum(results)}/{len(results)})")
        # also save to file (raw results and final scores), save to predictions path
        outfile_name = args.predictions_path.replace(".json", "_scores.json")
        with open(outfile_name, "w") as f:
            json.dump(
                {
                    "ex_results": results,
                    "valid_percentage": valid_percentage,
                    "ex_match": average_score,
                },
                f,
            )
    else:
        print("No valid samples processed")


if __name__ == "__main__":
    main()

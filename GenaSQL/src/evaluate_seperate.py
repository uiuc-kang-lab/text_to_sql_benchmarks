#!/usr/bin/env python
import yaml
import argparse
import json
import os
from typing import Dict, List, Any

import tqdm

from loguru import logger

from text2sql.data.datasets import SqliteDataset
from text2sql.evaluation.metrics.execution_match import execution_match
from run import Candidate, CandidateList

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
        "--candidates-folder",
        type=str,
        default="../results-dev-subset-1/4_candidate_generation",
        help="Path to the candidates folder containing model predictions",
    )
    parser.add_argument(
        "--candidate-configs-path",
        type=str,
        default="./bird_data/consistency_candidate_configs.yaml",
        help="path to the candidate configs file",
    )
    args = parser.parse_args()

    # Create SQLiteDataset
    dataset = SqliteDataset(args.test_database_path)

    # Load test data
    with open(args.test_json_path, "r") as f:
        test_data = json.load(f)

    # Load candidates
    candidates = {}
    for file in os.listdir(args.candidates_folder):
        if os.path.basename(file).startswith("candidates_qid-") and file.endswith(".json"):
            question_id = int(file.rsplit(".", 1)[0].rsplit("-", 1)[-1])
            with open(os.path.join(args.candidates_folder, file), "r") as f:
                candidate_list = CandidateList.model_validate_json(f.read())
                candidates[question_id] = candidate_list
            
    with open(args.candidate_configs_path, "r") as f:
        candidate_config_data: list[dict] = yaml.safe_load(f)
        if "configs" not in candidate_config_data:
            raise ValueError("candidate_config_data must contain a 'configs' key")
        if "top_k" in candidate_config_data:
            top_k = candidate_config_data["top_k"]
        candidate_configs: list[dict] = candidate_config_data["configs"]
    
    # Create a mapping from question_id to test data for easier lookup
    test_data_map = {int(item["question_id"]): item for item in test_data}

    # Dictionary to store all configuration results
    all_results = {}

    for idx, candidate_config in enumerate(candidate_configs):
        # Initialize result list
        results: list[int] = []
        valid_count: int = 0

        predictions = {question_id : candidate_list.candidates[idx].candidate_sql for question_id, candidate_list in candidates.items()}

        # Process each prediction
        for question_id, predicted_sql in tqdm.tqdm(predictions.items(), desc=f"Evaluating config_{idx+1}"):
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
                results.append(0)

        # Calculate scores for this configuration
        if len(results) > 0:
            average_score = sum(results) / len(results)
            valid_percentage = valid_count / len(results)
            print()
            print(f"Config {idx+1}:")
            print(f"Valid Percentage : {valid_percentage:.4f} ({valid_count}/{len(results)})")
            print(f"Execution Match  : {average_score:.4f} ({sum(results)}/{len(results)})")
            
            # Store results for this configuration
            all_results[f"config_{idx+1}"] = {
                # "ex_results": results,
                "valid_percentage": valid_percentage,
                "ex_match": average_score,
            }
        else:
            print(f"Config {idx+1}: No valid samples processed")

        # Save all results to a single JSON file
        results_path = os.path.join(os.path.dirname(args.candidates_folder), "results_seperate.json")
        with open(results_path, "w") as f:
            json.dump(all_results, f, indent=2)
        print(f"\nAll results saved to: {results_path}")

if __name__ == "__main__":
    main()

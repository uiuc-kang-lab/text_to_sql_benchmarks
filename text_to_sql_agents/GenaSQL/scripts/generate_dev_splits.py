#!/usr/bin/env python3
"""
Script to split a JSON dataset into multiple splits using round-robin assignment.
"""

import argparse
import json
import os
import random
from typing import Any, List


def load_json_data(file_path: str) -> List[dict[str, Any]]:
    """Load JSON data from a file."""
    with open(file_path, "r", encoding="utf-8") as f:
        return json.load(f)


def save_json_data(data: List[dict[str, Any]], file_path: str) -> None:
    """Save JSON data to a file."""
    with open(file_path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2)


def split_dataset_round_robin(data: List[dict[str, Any]], num_splits: int) -> List[List[dict[str, Any]]]:
    """Split dataset using round-robin assignment."""
    if num_splits <= 0:
        raise ValueError("Number of splits must be positive")

    if num_splits > len(data):
        raise ValueError(f"Number of splits ({num_splits}) cannot be greater than dataset size ({len(data)})")

    # Initialize empty splits
    splits = [[] for _ in range(num_splits)]

    # Assign items round-robin
    for i, item in enumerate(data):
        split_idx = i % num_splits
        splits[split_idx].append(item)

    return splits


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Split a JSON dataset into multiple splits using round-robin assignment"
    )
    parser.add_argument("--input-file", type=str, required=True, help="path to the input JSON file")
    parser.add_argument("--num-splits", type=int, required=True, help="number of splits to create from the dataset")
    parser.add_argument("--output-dir", type=str, required=True, help="output directory for split JSON files")
    parser.add_argument("--shuffle", action="store_true", help="if set, shuffle the data before splitting")
    args = parser.parse_args()

    # Load the dataset
    print(f"Loading dataset from {args.input_file}")
    data = load_json_data(args.input_file)
    print(f"Loaded {len(data)} samples")

    # Shuffle if requested
    if args.shuffle:
        print("Shuffling dataset")
        random.shuffle(data)

    # Split the dataset using round-robin assignment
    splits = split_dataset_round_robin(data, args.num_splits)
    print(f"Split dataset into {args.num_splits} splits of lengths: {[len(split) for split in splits]}")

    # Create output directory if it doesn't exist
    os.makedirs(args.output_dir, exist_ok=True)

    # Get the base filename without extension
    input_filename = os.path.basename(args.input_file)
    base_name = os.path.splitext(input_filename)[0]

    # Save each split
    for i, split_data in enumerate(splits):
        # Format the split number with leading zeros (e.g., 01, 02, etc.)
        split_num = f"{i+1:02d}"
        output_filename = f"{base_name}.split-{split_num}-of-{args.num_splits:02d}.json"
        output_path = os.path.join(args.output_dir, output_filename)
        save_json_data(split_data, output_path)
        print(f"Saved split {i+1}/{args.num_splits} to {output_path}")
    print("Done!")


if __name__ == "__main__":
    main()

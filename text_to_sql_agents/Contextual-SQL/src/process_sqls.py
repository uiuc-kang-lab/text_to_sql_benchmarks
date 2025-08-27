#!/usr/bin/env python3
"""
SQL Processing Controller - Runs SQL processing with auto-restart until completion.
"""

import argparse
import os
import subprocess
import multiprocessing
import time


NUM_CPUS = round(multiprocessing.cpu_count() * 0.4)


def count_lines(file_path: str) -> int:
    """Count lines in file, return 0 if file doesn't exist."""
    try:
        with open(file_path, "r") as f:
            return sum(1 for _ in f)
    except FileNotFoundError:
        return 0


def run_sql_processor(
        data_file: str, num_prompts_per_query: int, generations_dir: str, output_dir: str, sql_timeout: float = 40.0, timeout: int = 3600, compare_against_gt: bool = False, ignore_timeouts_from_cache: bool = False
) -> bool:
    """Run the SQL processing script with timeout."""
    # Setup environment and parameters
    env = os.environ.copy()
    env["PYTHONPATH"] = f"{os.getcwd()}/src:{env.get('PYTHONPATH', '')}"
    env["TOKENIZERS_PARALLELISM"] = "false"

    num_data = count_lines(data_file)

    cmd = [
        "python",
        "src/process_sqls_helper.py",
        "--file_pattern",
        f"{generations_dir}/data_gen*.jsonl",
        "--total_length",
        str(num_data * num_prompts_per_query),
        "--output_file",
        f"{output_dir}/data_with_results.jsonl",
        "--output_cache_file",
        f"{output_dir}/sql_results_cache.json",
        "--poll_interval",
        "5.0",
        "--time_out",
        str(sql_timeout),
        "--num_cpus",
        str(NUM_CPUS),
    ]
    if compare_against_gt:
        cmd.append("--compare_against_gt")
    if ignore_timeouts_from_cache:
        cmd.append("--ignore_timeouts_from_cache")

    try:
        result = subprocess.run(
            cmd, env=env, timeout=timeout, text=True
        )
        return result.returncode == 0
    except subprocess.TimeoutExpired:
        print(f"⏰ Process timed out ({timeout}s), restarting...")
        return False
    except Exception as e:
        print(f"❌ Process failed: {e}")
        return False


def parse_args():
    """Parse command line arguments."""
    parser = argparse.ArgumentParser(
        description="SQL Processing Controller with auto-restart",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    )
    parser.add_argument(
        "--input_file", required=True, help="Input data file to process"
    )
    parser.add_argument(
        "--generations_dir",
        required=True,
        help="Directory to read generations from",
    )
    parser.add_argument(
        "--output_dir", required=True, help="Directory to write processed results"
    )
    parser.add_argument(
        "--num_prompts_per_query", type=int, default=32, help="Number of prompts per query"
    )
    parser.add_argument(
        "--sql_timeout",
        type=float,
        default=40.0,
        help="Timeout in seconds for each SQL query",
    )
    parser.add_argument(
        "--timeout",
        type=float,
        default=3600.0,
        help="Timeout in seconds for each processing run",
    )
    parser.add_argument(
        "--retry_delay",
        type=float,
        default=2.0,
        help="Delay in seconds before retrying after failure",
    )
    parser.add_argument(
        "--compare_against_gt",
        action="store_true",
        help="Compare against ground truth",
    )
    parser.add_argument(
        "--rerun_but_use_cache",
        action="store_true",
        help="Rerun but use cache",
    )
    parser.add_argument(
        "--ignore_timeouts_from_cache",
        action="store_true",
        help="Ignore timeouts from cache",
    )
    return parser.parse_args()


def main():
    """Main loop: run processor until all entries are processed."""
    args = parse_args()

    # Setup
    target_count = count_lines(args.input_file)

    print(f"🎯 Target: {target_count} entries")
    print(f"🔧 Using {NUM_CPUS} CPU cores")
    print(f"⏱️  Timeout: {args.timeout}s per run")
    if args.rerun_but_use_cache:
        print("⏳ Rerun but use cache")
    if args.ignore_timeouts_from_cache:
        print("⏳ Ignoring timeouts from cache")
    if args.compare_against_gt:
        print("⏳ Comparing against ground truth")
    print("=" * 40)

    if args.rerun_but_use_cache:
        if os.path.exists(args.output_dir + "/data_with_results.jsonl"):
            os.remove(args.output_dir + "/data_with_results.jsonl")
            print("✅ Removed output file")

    # Process until complete
    while True:
        current_count = count_lines(args.output_dir + "/data_with_results.jsonl")

        # Check if done
        if current_count >= target_count:
            print(f"✅ Complete! Processed {current_count}/{target_count} entries")
            break

        # Show progress and run processor
        print(f"📊 Progress: {current_count}/{target_count} entries")
        success = run_sql_processor(
            args.input_file, args.num_prompts_per_query, args.generations_dir, args.output_dir, args.sql_timeout, args.timeout, args.compare_against_gt, args.ignore_timeouts_from_cache
        )

        # Check if we made progress
        new_count = count_lines(args.output_dir + "/data_with_results.jsonl")
        if new_count > current_count:
            print(f"✨ Progress: +{new_count - current_count} entries")
        elif not success:
            print(f"🔄 No progress, retrying in {args.retry_delay} seconds...")
            time.sleep(args.retry_delay)


if __name__ == "__main__":
    main()

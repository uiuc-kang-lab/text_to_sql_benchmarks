import argparse
import copy
import glob
import io
from hashlib import md5
import json
import multiprocessing
import os
import sqlite3
import statistics
import sys
import time
from contextlib import redirect_stderr, suppress
from multiprocessing import Pool, TimeoutError

from func_timeout import FunctionTimedOut, func_timeout
from tqdm import tqdm

NUM_LINES_BATCH_SIZE = 2000
connections = {}


def worker_init():
    global connections
    connections = {}  # brand new for each worker process


def worker_run_sql_helper(conn, sql, gt_sql, max_chars):
    """
    Actual SQL execution logic (no timeout logic here, just the raw query).
    We call this inside func_timeout to limit runtime in worker_run_sql.
    """
    cursor = conn.cursor()

    cursor.execute(sql)
    predicted_res = set(cursor.fetchall())

    if gt_sql is not None:
        cursor.execute(gt_sql)
        gt_res = set(cursor.fetchall())

    # Sort results in some stable manner
    def none_last_str(row):
        return tuple((item is None, "" if item is None else str(item)) for item in row)

    predicted_res_sorted = sorted(predicted_res, key=none_last_str)
    predicted_res_hash = md5(str(predicted_res_sorted).encode("utf-8")).hexdigest()

    # Turn them into a truncated TSV string
    tsv = get_tsv_from_list_of_list(predicted_res_sorted)
    subsample_factor = (len(tsv) // max_chars) + 1

    if len(predicted_res) == 0:
        evaluation = "pass: incorrect-empty"
        result_str = ""
        result_hash = ""
        num_rows = 0
    else:
        if gt_sql is not None:
            if predicted_res == gt_res:
                evaluation = "pass: correct"
            else:
                evaluation = "pass: incorrect"
        else:
            evaluation = "pass: ??"
        sampled_rows = predicted_res_sorted[::subsample_factor]
        result_str = get_tsv_from_list_of_list(sampled_rows)[:max_chars]
        result_hash = predicted_res_hash
        num_rows = len(predicted_res_sorted)

    return (evaluation, result_str, result_hash, num_rows)


def worker_run_sql(task):
    """
    Worker function that receives one query:
      task = (db_path, sql, gt_sql, max_chars, time_out)
    Execute the SQL under a timeout, and return:
      (db_path, sql, evaluation, result_str, result_hash, num_rows, elapsed_time).
    """
    db_path, sql, gt_sql, max_chars, time_out = task

    global connections
    if db_path not in connections:
        # Create and store a single connection per db_path
        connections[db_path] = sqlite3.connect(db_path, check_same_thread=False)

    conn = connections[db_path]
    start_time = time.time()

    stderr = io.StringIO()
    with suppress(RuntimeError, ReferenceError), redirect_stderr(stderr):
        try:
            evaluation, result_str, result_hash, num_rows = func_timeout(
                time_out, worker_run_sql_helper, args=(conn, sql, gt_sql, max_chars)
            )
        except KeyboardInterrupt:
            sys.exit(0)
        except FunctionTimedOut:
            evaluation, result_str, result_hash, num_rows = ("error: timeout", "", "", 0)
        except Exception as e:
            evaluation, result_str, result_hash, num_rows = (
                "error: <error>",
                f"Execution error: {e}",
                "",
                0,
            )

    elapsed_time = time.time() - start_time
    return (db_path, sql, evaluation, result_str, result_hash, num_rows, elapsed_time)


###############################################################################
# Helper / Utility
###############################################################################
def get_tsv_from_list_of_list(data):
    return "\n".join(
        [
            "\t".join([str(x) if not isinstance(x, float) else f"{x:.3f}" for x in row])
            for row in data
        ]
    )


def compute_time_stats(times):
    """
    Given a list of elapsed times, compute count, mean, median, p95, p99.
    Return a string summarizing these stats.
    """
    if not times:
        return "No data"
    times_sorted = sorted(times)
    n = len(times_sorted)
    mean_ = sum(times_sorted) / n
    median_ = statistics.median(times_sorted)
    i95 = min(int(0.95 * n), n - 1)
    i99 = min(int(0.99 * n), n - 1)
    p95_ = times_sorted[i95]
    p99_ = times_sorted[i99]
    return (
        f"count={n}, mean={mean_:.4f}, median={median_:.4f}, "
        f"p95={p95_:.4f}, p99={p99_:.4f}"
    )


###############################################################################
# Main function
###############################################################################
def main():
    parser = argparse.ArgumentParser(
        description="Periodically read .jsonl files, merge data, run SQL with timeout, output once at end."
    )
    parser.add_argument(
        "--file_pattern",
        required=True,
        help="Glob pattern for jsonl files (e.g. '/path/to/data-*.jsonl')",
    )
    parser.add_argument(
        "--total_length",
        type=int,
        required=True,
        help="Total number of lines to process before stopping.",
    )
    parser.add_argument(
        "--output_file", required=True, help="Path to single jsonl output file."
    )
    parser.add_argument(
        "--output_cache_file",
        required=True,
        help="Path to JSON file for caching results (db_path+SQL).",
    )
    parser.add_argument(
        "--poll_interval",
        type=float,
        default=5.0,
        help="Seconds to wait between file reads if total_length not reached.",
    )
    parser.add_argument(
        "--num_cpus", type=int, default=1, help="Number of worker processes."
    )
    parser.add_argument(
        "--time_out", type=float, default=30.0, help="Per-query timeout in seconds."
    )
    parser.add_argument(
        "--max_chars",
        type=int,
        default=8092,
        help="Max characters in the returned result TSV.",
    )
    parser.add_argument(
        "--compare_against_gt",
        action="store_true",
        help="Compare against ground truth",
    )
    parser.add_argument(
        "--ignore_timeouts_from_cache",
        action="store_true",
        help="Ignore timeouts from cache",
    )
    args = parser.parse_args()

    file_pattern = args.file_pattern
    total_length = args.total_length
    output_file = args.output_file
    poll_interval = args.poll_interval
    os.makedirs(os.path.dirname(args.output_file), exist_ok=True)
    os.makedirs(os.path.dirname(args.output_cache_file), exist_ok=True)

    # Tracks how many lines we've actually read (including duplicates)
    lines_processed = 0

    # For each file, track how many bytes we have read so far:
    file_offsets = {}

    # -------------------------------------------------------------------------
    # merged_data will hold the final merged lines in memory.
    # Key = (question_id, db_id)
    # Value = a dict shaped like:
    # {
    #   "question_id": <value>,
    #   "db_id": <value>,
    #   "db_path": <value>,
    #   "responses": {
    #       sql_str: {
    #          "content": sql_str,
    #          "sources": [...],
    #          "all_logprobs": [...],
    #          "evaluation": <str or None>,
    #          "result": <str or None>,
    #          "num_rows": <int or None>,
    #       },
    #       ...
    #   }
    # }
    # -------------------------------------------------------------------------
    merged_data = {}

    # -------------------------------------------------------------------------
    # results_cache is where we store precomputed results. Key = (db_path, sql)
    # Value = {
    #   "evaluation": <str>,
    #   "result": <str>,
    #   "num_rows": <int>
    # }
    # This lets us skip re-running the same (db_path, sql) if we already have it.
    # -------------------------------------------------------------------------
    results_cache = {}
    # Load output_cache_file:
    if os.path.isfile(args.output_cache_file):
        try:
            num_cache_discarded = 0
            with open(args.output_cache_file, "r", encoding="utf-8") as cache_f:
                # Example structure in JSON:
                # {
                #   "db_path<$$|||$$>SQL": {"evaluation": "...", "result": "...", "num_rows": ...},
                #   ...
                # }
                raw_cache = json.load(cache_f)
                for key_str, val in raw_cache.items():
                    dbpath_sql = tuple(key_str.split("<$$|||$$>", 1))
                    if args.ignore_timeouts_from_cache and val["evaluation"] == "error: timeout":
                        num_cache_discarded += 1
                        continue
                    results_cache[dbpath_sql] = val
            print(f"[INFO] Discarded {num_cache_discarded} entries from cache due to timeout")
            print(
                f"[INFO] Loaded existing cache with {len(results_cache)} entries from {args.output_cache_file}"
            )
        except Exception as e:
            print(f"[WARN] Could not load cache file {args.output_cache_file}: {e}")

    # We'll keep track of per-db timing stats in the main process
    db_timing_stats = {}  # db_path -> list of float (elapsed times)

    # We'll keep track of evaluation counts:
    evaluation_counts = {}  # evaluation_str -> int

    # Create a multiprocessing pool
    pool = Pool(processes=args.num_cpus, initializer=worker_init)

    # -------------------------------------------------------------------------
    # Read lines in a loop until we process 'total_length' lines
    # Merge them in-memory, and only run new queries each time.
    # We do NOT write out the lines yet.
    # -------------------------------------------------------------------------
    while lines_processed < total_length:
        all_files = sorted(glob.glob(file_pattern))

        iteration_lines = 0  # number of lines read in *this* iteration
        queries_batch = []  # holds tasks for new queries only

        for fpath in all_files:
            if iteration_lines >= NUM_LINES_BATCH_SIZE:
                # Already reached the max for this iteration
                break

            if fpath not in file_offsets:
                file_offsets[fpath] = 0

            try:
                fsize = os.path.getsize(fpath)
            except OSError:
                continue

            # Skip if no new content in this file
            if fsize <= file_offsets[fpath]:
                continue

            with open(fpath, "r", encoding="utf-8") as f:
                f.seek(file_offsets[fpath])

                # Read lines up to NUM_LINES_BATCH_SIZE lines for this iteration, or until total_length
                while (
                    iteration_lines < NUM_LINES_BATCH_SIZE
                    and lines_processed < total_length
                ):
                    line = f.readline()
                    if not line:
                        break  # no more lines in this file

                    line = line.strip()
                    if not line:
                        print(f"[WARN] Empty line in {fpath}")
                        continue

                    # Attempt to parse
                    try:
                        datum = json.loads(line)
                    except json.JSONDecodeError:
                        print(f"[WARN] Invalid JSON in {fpath}: {line}")
                        continue

                    question_id = datum.get("question_id")
                    db_id = datum.get("db_id")
                    db_path = datum.get("db_path")
                    gt_sql = datum.get("SQL")
                    responses = datum.get("responses", {})

                    if (
                        (question_id is None)
                        or (db_id is None)
                        or (db_path is None)
                        or (responses is None)
                    ):
                        print(
                            f"[WARN] Missing question_id, db_id, db_path, or responses in {fpath} line."
                        )
                        continue

                    if args.compare_against_gt:
                        if gt_sql is None or gt_sql == "":
                            print(f"[WARN] Missing gt_sql in {fpath} line.")
                            continue

                    # Merge logic
                    key = (question_id, db_id)
                    if key not in merged_data:
                        # Make a deep copy to preserve structure
                        merged_data[key] = copy.deepcopy(datum)
                        # We'll force the shape to ensure "responses" is a dict
                        merged_data[key]["responses"] = {}

                    # For each SQL response, merge or add
                    merged_responses = merged_data[key]["responses"]
                    for sql_str, resp_data in responses.items():
                        if sql_str not in merged_responses:
                            # It's a new response: add
                            merged_responses[sql_str] = {
                                "content": sql_str,
                                "sources": resp_data.get("sources", []),
                                "all_logprobs": resp_data.get("all_logprobs", []),
                                "evaluation": None,
                                "result": None,
                                "result_hash": None,
                                "num_rows": None,
                            }
                        else:
                            # Already have a response in memory
                            existing_resp = merged_responses[sql_str]
                            # Extend sources and logprobs
                            existing_resp["sources"].extend(
                                resp_data.get("sources", [])
                            )
                            existing_resp["all_logprobs"].extend(
                                resp_data.get("all_logprobs", [])
                            )

                        # Check if we already have a cache entry for (db_path, sql_str)
                        # If so, skip re-running in queries_batch. We'll just set the data from the cache
                        db_sql_key = (db_path, sql_str)
                        if db_sql_key in results_cache:
                            # We have a precomputed result
                            cached_evaluation = results_cache[db_sql_key]["evaluation"]
                            cached_result = results_cache[db_sql_key]["result"]
                            cached_result_hash = results_cache[db_sql_key]["result_hash"]
                            cached_num_rows = results_cache[db_sql_key]["num_rows"]

                            # Populate merged_data from the cache
                            merged_responses[sql_str]["evaluation"] = cached_evaluation
                            merged_responses[sql_str]["result"] = cached_result
                            merged_responses[sql_str]["result_hash"] = cached_result_hash
                            merged_responses[sql_str]["num_rows"] = cached_num_rows

                        # If no evaluation in memory (and not in the cache),
                        # or if "evaluation" is still None => we must queue a query
                        if merged_responses[sql_str]["evaluation"] is None:
                            queries_batch.append(
                                (db_path, sql_str, gt_sql if args.compare_against_gt else None, args.max_chars, args.time_out)
                            )

                    iteration_lines += 1
                    lines_processed += 1
                    file_offsets[fpath] = f.tell()

                    if lines_processed >= total_length:
                        break

            if (
                lines_processed >= total_length
                or iteration_lines >= NUM_LINES_BATCH_SIZE
            ):
                break

        # ---------------------------------------------------------------------
        # Now we have merged everything read this iteration.
        # Next, we only run queries for new or not-yet-evaluated responses.
        # ---------------------------------------------------------------------
        if iteration_lines > 0:
            print(
                f"[INFO] Read {iteration_lines} new lines in this iteration. "
                f"Total lines processed so far: {lines_processed}/{total_length}."
            )

            # Distinct aggregator entries = how many unique (question_id, db_id) so far
            distinct_entries_count = len(merged_data)

            if distinct_entries_count > 0:
                # Compute average # of SQLs in each merged entry
                total_sql_count = sum(
                    len(d_obj["responses"]) for d_obj in merged_data.values()
                )
                avg_sql_count = total_sql_count / distinct_entries_count

                print(
                    f"[INFO] We currently have {distinct_entries_count} distinct merged entries in memory. "
                    f"Average #SQLs per entry: {avg_sql_count:.2f}"
                )

            if queries_batch:
                print("[INFO] Creating pool...")
                pool = Pool(processes=args.num_cpus, initializer=worker_init)
                print("[INFO] Pool created...")

                print(
                    f"[INFO] Will run {len(queries_batch)} SQL queries in parallel on {args.num_cpus} CPUs..."
                )
                # Use apply_async with a list to collect all async results
                async_results = [
                    pool.apply_async(worker_run_sql, (task,)) for task in queries_batch
                ]

                # Initialize a list to store successfully processed results
                successful_results = []

                for res_num, async_res in tqdm(
                    enumerate(async_results),
                    total=len(async_results),
                    desc="Running SQL",
                ):
                    try:
                        # Wait for the result with timeout. There is func_timeout so this is redundant. In case, threads are blocked.
                        outcome = async_res.get(timeout=2.0 * args.time_out)
                        successful_results.append(outcome)

                        dbp, s, evaluation, result_str, result_hash, num_rows, elapsed_time = outcome

                        # Store the timing info
                        if dbp not in db_timing_stats:
                            db_timing_stats[dbp] = []
                        db_timing_stats[dbp].append(elapsed_time)

                        # Count the evaluation
                        evaluation_counts[evaluation] = (
                            evaluation_counts.get(evaluation, 0) + 1
                        )

                        # Update merged_data with the result
                        for (q_id, d_id), data_obj in merged_data.items():
                            if data_obj["db_path"] == dbp:
                                responses_map = data_obj["responses"]
                                if s in responses_map:
                                    responses_map[s]["evaluation"] = evaluation
                                    responses_map[s]["result"] = result_str
                                    responses_map[s]["result_hash"] = result_hash
                                    responses_map[s]["num_rows"] = num_rows
                    except TimeoutError:
                        print(f"[WARN] Task timed out after {args.time_out} seconds.")
                        # timeouts_in_iteration += 1
                        dbp, s, _, _, _ = queries_batch[res_num]
                        evaluation, result_str, result_hash, num_rows, elapsed_time = (
                            "error: timeout",
                            "",
                            "",
                            0,
                            args.time_out,
                        )

                    # Also update the results_cache
                    db_sql_key = (dbp, s)
                    results_cache[db_sql_key] = {
                        "evaluation": evaluation,
                        "result": result_str,                        
                        "result_hash": result_hash,
                        "num_rows": num_rows,
                    }

                print("[INFO] Closing pool...")
                pool.close()
                pool.join()
                print("[INFO] Closed pool...")

                # -----------------------------------------------------------------
                # After each iteration, we update the output_cache_file
                # -----------------------------------------------------------------
                try:
                    # Convert results_cache to a dictionary-of-dicts for JSON
                    cache_dict = {}
                    for (dbp_, sql_), cvals in results_cache.items():
                        key_str = f"{dbp_}<$$|||$$>{sql_}"
                        cache_dict[key_str] = cvals
                    with open(args.output_cache_file, "w", encoding="utf-8") as cfile:
                        json.dump(cache_dict, cfile, ensure_ascii=False)
                    print(f"[INFO] Updated cache file with {len(cache_dict)} entries.")
                except Exception as e:
                    print(
                        f"[WARN] Failed to write cache file {args.output_cache_file}: {e}"
                    )

                # Print DB timing stats
                print("[INFO] Per-DB execution time stats (so far):")
                for dbp, times_list in db_timing_stats.items():
                    stats_str = compute_time_stats(times_list)
                    print(f"  DB: {dbp} => {stats_str}")

                # Print the evaluation counts so far
                print("[INFO] Evaluation result counts (so far):")
                for ev_key, ev_count in evaluation_counts.items():
                    print(f"  {ev_key} => {ev_count}")

                # Optionally, you can handle re-queuing of timed-out tasks here
                # For simplicity, we're skipping them

            else:
                print("[INFO] No new queries to run this iteration.")

        if lines_processed < total_length and iteration_lines == 0:
            # We found no new lines, so sleep
            print(f"[INFO] No new lines found. Sleeping {poll_interval} sec...")
            time.sleep(poll_interval)

    print("[INFO] Finalizing output...")
    # Final cache update in case there are any last-second merges
    try:
        cache_dict = {}
        for (dbp_, sql_), cvals in results_cache.items():
            key_str = f"{dbp_}<$$|||$$>{sql_}"
            cache_dict[key_str] = cvals
        with open(args.output_cache_file, "w", encoding="utf-8") as cfile:
            json.dump(cache_dict, cfile, ensure_ascii=False)
        print(f"[INFO] Final cache update => {len(cache_dict)} entries saved.")
    except Exception as e:
        print(f"[WARN] Failed final cache file write: {e}")

    # We can now write out one merged line per (question_id, db_id).
    with open(output_file, "w", encoding="utf-8") as outf:
        for (q_id, d_id), data_obj in merged_data.items():
            outf.write(json.dumps(data_obj, ensure_ascii=False) + "\n")

    print(
        f"Done. Processed {lines_processed} lines total. Merged output has {len(merged_data)} lines."
    )
    print(f"Output saved to {output_file}.")

    # Final print of the aggregated evaluation counts
    print("[INFO] Final evaluation result counts:")
    for ev_key, ev_count in evaluation_counts.items():
        print(f"  {ev_key} => {ev_count}")


###############################################################################
# Entry Point
###############################################################################
if __name__ == "__main__":
    # For cleaner Ctrl+C handling on some systems:
    multiprocessing.set_start_method("spawn", force=True)
    main()

from pathlib import Path

import orjson
import csv


def read_json_file(file):
    """this util will do the right thing depending on whether the file has the .json or the .jsonl extension"""
    suffix = Path(file).suffix[1:]
    with open(file, "rb") as f:
        if suffix == "jsonl":
            return [orjson.loads(line) for line in f]
        elif suffix == "json":
            return orjson.loads(f.read())
        else:
            raise ValueError(
                f"Expected 'jsonl' or 'json' file extension but got: {suffix}"
            )


def read_jsonl_file(path):
    """Reads a JSONL file, returns a list of dictionaries."""
    data_list = []
    with open(path, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            data_list.append(orjson.loads(line))
    return data_list


def write_json_file(file, data, indent=False):
    """this util will do the right thing depending on whether the file has the .json or the .jsonl extension"""
    suffix = Path(file).suffix[1:]
    opts = orjson.OPT_APPEND_NEWLINE  # auto-adds a new line
    if indent:
        opts |= orjson.OPT_INDENT_2
    with open(file, "wb") as f:
        if suffix == "jsonl":
            for output in data:
                f.write(orjson.dumps(output, option=opts))
        elif suffix == "json":
            f.write(orjson.dumps(data, option=opts))
        else:
            raise ValueError(f"Expected 'jsonl' or 'json' but got: {suffix}")


def append_jsonl_file(path, data_list):
    """
    Appends each item in data_list to path as JSONL lines.
    Creates the file if it doesn't exist.
    """
    with open(path, "a", encoding="utf-8") as f:
        for item in data_list:
            line_bytes = orjson.dumps(item)
            line_str = line_bytes.decode("utf-8")
            f.write(line_str + "\n")


def write_jsonl_file(path, data_list):
    """
    Write each item in data_list to path as JSONL lines.
    Overwrites the file if it exists.
    """
    with open(path, "w", encoding="utf-8") as f:
        for item in data_list:
            line_bytes = orjson.dumps(item)
            line_str = line_bytes.decode("utf-8")
            f.write(line_str + "\n")


def read_tsv_file(file_path):
    """Reads a TSV file using the csv module."""
    data = []
    with open(file_path, 'r', encoding='utf-8') as tsvfile:
        reader = csv.reader(tsvfile, delimiter='\t')
        for row in reader:
            data.append(row)
    return data

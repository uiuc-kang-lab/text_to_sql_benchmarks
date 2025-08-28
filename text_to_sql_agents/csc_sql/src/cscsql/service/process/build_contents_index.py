import argparse
import json
import os, shutil
import sqlite3
from func_timeout import func_set_timeout, FunctionTimedOut
from pathlib import Path


# get the database cursor for a sqlite database path
def get_cursor_from_path(sqlite_path):
    try:
        if not os.path.exists(sqlite_path):
            print("Open a new connection %s" % sqlite_path)
        connection = sqlite3.connect(sqlite_path, check_same_thread=False)
    except Exception as e:
        print(sqlite_path)
        raise e
    connection.text_factory = lambda b: b.decode(errors="ignore")
    cursor = connection.cursor()
    return cursor


# execute predicted sql with a long time limitation (for building content index)
@func_set_timeout(3600)
def execute_sql(cursor, sql):
    cursor.execute(sql)

    return cursor.fetchall()


def remove_contents_of_a_folder(index_path):
    # if index_path does not exist, then create it
    os.makedirs(index_path, exist_ok=True)
    # remove files in index_path
    for filename in os.listdir(index_path):
        file_path = os.path.join(index_path, filename)
        try:
            if os.path.isfile(file_path) or os.path.islink(file_path):
                os.unlink(file_path)
            elif os.path.isdir(file_path):
                shutil.rmtree(file_path)
        except Exception as e:
            print('Failed to delete %s. Reason: %s' % (file_path, e))


def is_number(s):
    try:
        float(s)
        return True
    except ValueError:
        return False


def build_content_index(db_file_path: str, index_path: str):
    '''
    create BM25 index for all string values in a database
    '''
    cursor = get_cursor_from_path(db_file_path)
    results = execute_sql(cursor, "SELECT name FROM sqlite_master WHERE type='table';")
    table_names = [result[0] for result in results]

    all_column_contents = []
    for table_name in table_names:
        # skip SQLite system table: sqlite_sequence
        if table_name == "sqlite_sequence":
            continue
        results = execute_sql(cursor, f"SELECT name FROM PRAGMA_TABLE_INFO('{table_name}')")
        column_names_in_one_table = [result[0] for result in results]
        for column_name in column_names_in_one_table:
            try:
                print(f"SELECT DISTINCT `{column_name}` FROM `{table_name}` WHERE `{column_name}` IS NOT NULL;")
                results = execute_sql(cursor,
                                      f"SELECT DISTINCT `{column_name}` FROM `{table_name}` WHERE `{column_name}` IS NOT NULL;")
                column_contents = [result[0] for result in results if
                                   isinstance(result[0], str) and not is_number(result[0])]

                for c_id, column_content in enumerate(column_contents):
                    # remove empty and extremely-long contents
                    if len(column_content) != 0 and len(column_content) <= 40:
                        all_column_contents.append(
                            {
                                "id": "{}-**-{}-**-{}".format(table_name, column_name, c_id),  # .lower()
                                "contents": column_content
                            }
                        )
            except Exception as e:
                print(str(e))

    temp_db_index_path = os.path.join(index_path, "temp_db_index")
    os.makedirs(temp_db_index_path, exist_ok=True)

    temp_content_path = f"{temp_db_index_path}/contents.json"

    with open(temp_content_path, "w") as f:
        f.write(json.dumps(all_column_contents, indent=2, ensure_ascii=True))

    os.makedirs(index_path, exist_ok=True)
    # Building a BM25 Index (Direct Java Implementation), see https://github.com/castorini/pyserini/blob/master/docs/usage-index.md
    cmd = f'python -m pyserini.index.lucene --collection JsonCollection --input {temp_db_index_path} --index "{index_path}" --generator DefaultLuceneDocumentGenerator --threads 16 --storePositions --storeDocvectors --storeRaw'

    d = os.system(cmd)
    print(d)
    os.remove(temp_content_path)


def build_index_for_dataset(dataset_name: str, db_path: str, save_index_path: str):
    print(f"build index for dataset: {dataset_name}")
    remove_contents_of_a_folder(save_index_path)
    # build content index
    db_ids = os.listdir(db_path)
    for db_id in db_ids:
        db_file_path = os.path.join(db_path, db_id, db_id + ".sqlite")
        if os.path.exists(db_file_path) and os.path.isfile(db_file_path):
            print(f"db_id: {db_id}, The file '{db_file_path}' exists.")
            build_content_index(
                db_file_path,
                os.path.join(save_index_path, db_id)
            )
        else:
            print(f"The file '{db_file_path}' does not exist.")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Build BM25 index for database values")
    parser.add_argument('--dataset_name', type=str, default="bird", help="dataset name")
    parser.add_argument('--db_path', type=str, help="db path")
    parser.add_argument('--save_index_path', type=str, help="save index path")

    args = parser.parse_args()
    print(f"Build BM25 index for database values, args: {args}")

    build_index_for_dataset(
        dataset_name=args.dataset_name,
        db_path=args.db_path,
        save_index_path=args.save_index_path
    )

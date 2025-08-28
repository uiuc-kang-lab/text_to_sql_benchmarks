#!/bin/bash
set -v
set -e

DATASET_NAME="bird"
DATASET_BASE_DIR=${HOME}/work

# for BIRD dev
DATASET_MODE="dev"
DATAFILE_PATH="${DATASET_BASE_DIR}/bird/dev_20240627/dev.json"
DATASET_PATH="${DATASET_BASE_DIR}/bird/dev_20240627/dev_databases"
TABLES_PATH="${DATASET_BASE_DIR}/bird/dev_20240627/dev_tables.json"
SAVE_INDEX_PATH="${DATASET_BASE_DIR}/bird/dev_20240627/db_contents_index"
PROMPT_OUTPUT_PATH="${DATASET_BASE_DIR}/bird/dev_20240627/dev_bird.json"


## for BIRD test
#DATASET_MODE="test"
#DATAFILE_PATH="${DATASET_BASE_DIR}/bird/test/test.json"
#DATASET_PATH="${DATASET_BASE_DIR}/bird/test/test_databases"
#TABLES_PATH="${DATASET_BASE_DIR}/bird/test/test_tables.json"
#SAVE_INDEX_PATH="${DATASET_BASE_DIR}/bird/test/db_contents_index"
#PROMPT_OUTPUT_PATH="${DATASET_BASE_DIR}/bird/test/test_bird.json"

## for BIRD train
#DATASET_MODE="train"
#DATAFILE_PATH="${DATASET_BASE_DIR}/bird/train/train.json"
#DATASET_PATH="${DATASET_BASE_DIR}/bird/train/train_databases"
#TABLES_PATH="${DATASET_BASE_DIR}/bird/train/train_tables.json"
#SAVE_INDEX_PATH="${DATASET_BASE_DIR}/bird/train/db_contents_index"
#PROMPT_OUTPUT_PATH="${DATASET_BASE_DIR}/bird/train/train_bird.json"


python -m cscsql.service.process.process_dataset \
--input_data_file $DATAFILE_PATH \
--output_data_file $PROMPT_OUTPUT_PATH \
--db_path $DATASET_PATH \
--tables $TABLES_PATH \
--source $DATASET_NAME \
--mode $DATASET_MODE \
--value_limit_num 2 \
--db_content_index_path $SAVE_INDEX_PATH




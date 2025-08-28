#!/bin/bash

set -v
set -e

run_day=$(date "+%Y%m%d_%H%M")

begin_time=$(date "+%Y_%m_%d_%H_%M_%S")
echo "run train text2sql begin time = ${begin_time}"

USER_HOME=${HOME}
echo "user home dir: ${USER_HOME}"

TASK_NAME="CscSql_bird"
MODEL_NAME="CscSqlBird"

DATA_DIR_BASE="${USER_HOME}/CscSql"
LOG_DIR="${DATA_DIR_BASE}/outputs/logs/${MODEL_NAME}"
mkdir -p ${LOG_DIR}

WORK_DIR="${USER_HOME}/work/csc_sql"

INFERENCE_DEBUG="False"
SLEEP_SECOND=10
LOG_FILE="${LOG_DIR}/run_${MODEL_NAME}_${begin_time}.log"

mkdir -p ${DATA_DIR}
mkdir -p ${DATA_DIR_BASE}/outputs/logs

train_log="${LOG_DIR}/run_train_${begin_time}.log"
echo "train log file ${train_log}"


export ACCELERATE_LOG_LEVEL=info
export TOKENIZERS_PARALLELISM=True
export VLLM_USE_MODELSCOPE=True


CUDA_VISIBLE_DEVICES=0,1,2 nohup  accelerate launch \
--config_file recipes/accelerate_configs/zero2.yaml \
--num_processes=3 src/cscsql/service/grpo/nl2sql_grpo.py \
--config recipes/Qwen2.5-Coder-7B-Instruct/grpo/config_merge_rl.yaml \
 >> ${train_log} 2>&1 &

echo "tail -f ${train_log}"
echo "running"

echo "tail -f ${train_log}" > ${WORK_DIR}/bin/nl2sql/temp.log
echo "run tflog to tail -f log"


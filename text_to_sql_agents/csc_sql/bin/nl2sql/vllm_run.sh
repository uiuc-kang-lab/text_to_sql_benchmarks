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

LOG_FILE="${LOG_DIR}/run_${MODEL_NAME}_${begin_time}.log"

mkdir -p ${DATA_DIR_BASE}/outputs/logs

train_log="${LOG_DIR}/run_train_${begin_time}.log"
train_vllm_log="${LOG_DIR}/run_train_${begin_time}_vllm.log"
echo "train log file ${train_log}"

export VLLM_USE_MODELSCOPE=True

#MODEL_PATH="Qwen/Qwen2.5-Coder-7B-Instruct"
MODEL_PATH="Qwen/Qwen2.5-Coder-3B-Instruct"
#MODEL_PATH="XGenerationLab/XiYanSQL-QwenCoder-3B-2502"
#MODEL_PATH="XGenerationLab/XiYanSQL-QwenCoder-7B-2502"

CUDA_VISIBLE_DEVICES=3 trl vllm-serve \
--gpu_memory_utilization 0.95 \
--port 14000 \
--max_model_len 20000 \
--model $MODEL_PATH \
 >> ${train_vllm_log} 2>&1 &

echo "tail -f ${train_vllm_log}"
echo "running"

echo "tail -f ${train_vllm_log}" > ${WORK_DIR}/bin/nl2sql/temp_vllm.log
echo "run tflog to tail -f log"

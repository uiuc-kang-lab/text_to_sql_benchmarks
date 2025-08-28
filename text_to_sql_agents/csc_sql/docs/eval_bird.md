# csc sql eval bird

## Environment Setup
```shell
conda create -n torch_vllm python=3.12
conda activate torch_vllm

# install vllm
pip install torch vllm

# install flash-attention
pip install packaging ninja
pip install flash-attn --no-build-isolation

# install current project
cd csc_sql
pip install -e .
```


## download model
```shell
# 7b size SQL merge model:
modelscope download --model  cycloneboy/CscSQL-Merge-Qwen2.5-Coder-7B-Instruct

# 7b size SQL generation model:
modelscope download --model  cycloneboy/CscSQL-Grpo-Qwen2.5-Coder-7B-Instruct

# 32b size SQL generation model:
#modelscope download --model  XGenerationLab/XiYanSQL-QwenCoder-32B-2412 

```

## Model inference
> Need to modify the configuration in bin/process/run_pipeline.sh

### 7B model inference
```shell
# Modify the configuration in bin/process/run_pipeline.sh
# Note: You need to modify the database path configuration in bin/process/run_pipeline.sh!!! (You can directly modify the example ## for BIRD test)
# DATASET_BASE_DIR: Data set root path
# DATAFILE_PATH: Data file path
# GOLD_PATH: Real SQL file, when there is no GOLD file, set to none
# DATASET_PATH: Database file path
# TABLES_PATH: Data table file
# SAVE_INDEX_PATH: Index file path generated in the middle
# PROMPT_OUTPUT_PATH: Output prompt file path, here is the PROMPT_OUTPUT_PATH prompt file output by preprocessing
# OUTPUT_DIR: Output file root path, the root path of the last generated SQL
# CUDA_VISIBLE_DEVICES: Available cuda device id, default is 0
# TENSOR_PARALLEL_SIZE: Parallelism of vllm inference model, default is 1

# MODEL_SQL_MERGE: 7B SQL merge model path, default is: cycloneboy/CscSQL-Merge-Qwen2.5-Coder-7B-Instruct, can be changed to the path downloaded in advance
# MODEL_SQL_GENERATE: 7B SQL generation model path, default is: cycloneboy/CscSQL-Grpo-Qwen2.5-Coder-7B-Instruct, can be changed to the path downloaded in advance
# N_SQL_GENERATE: Number of SQL generated, 7B model, change to 64;

# cd csc_sql
bash bin/process/run_pipeline.sh

# Log printing, after the above command is executed, the nohup log execution command will be printed around the first line from the end, for example: "tail -f ./logs/run_train_2025_05_25_16_44_52.log"
# After the inference is completed, a subdirectory with the current execution timestamp will be created under the $OUTPUT_DIR path, in which the final SQL file is generated, reference: outputs/20250525_164452/sampling_think_sql_merge_pred_major_voting_sqls.sql
# After about 1-2 hours of execution, the last line will print the final SQL file path, "result_file", reference: outputs/20250525_164452/sampling_think_sql_merge_pred_major_voting_sqls.sql
# The name of the final generated SQL file is: sampling_think_sql_merge_pred_major_voting_sqls.sql
# The generated SQL file only contains SQL statements, no db_id
```

## Model evaluation (optional)
> Dev evaluation script

```shell
cd csc_sql

# Modify the configuration file: bin/process/run_eval.sh
# DATASET_BASE_DIR: Data set root path
# DATAFILE_PATH: Data file path
# GOLD_PATH: Real SQL file,
# DATASET_PATH: Database file path
# PREDICTED_SQL_PATH: Predicted SQL file path, the final generated SQL file of the previous reasoning, reference: outputs/20250525_164452/sampling_think_sql_merge_pred_major_voting_sqls.sql

bash bin/process/run_eval.sh

```
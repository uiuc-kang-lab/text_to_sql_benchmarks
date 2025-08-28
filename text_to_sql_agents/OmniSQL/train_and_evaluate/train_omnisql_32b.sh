set -e

LR=2e-4
EPOCHS=2
CONFIG_FILE="./accelerate_config_32b.yaml"
PER_DEVICE_TRAIN_BATCH_SIZE=2
MODEL_PATH="Qwen/Qwen2.5-Coder-32B-Instruct"
CKPT_NUM=10
BASE_NAME="omnisql_32b_lr${LR}_epochs${EPOCHS}-lora"
CKPT_DIR="./ckpts/$BASE_NAME"
LOG_DIR="./train_logs/$BASE_NAME"
DATASET_DIR="./data/train_synsql.json"

accelerate launch --main_process_port 10000 --config_file $CONFIG_FILE train.py \
    --per_device_train_batch_size $PER_DEVICE_TRAIN_BATCH_SIZE \
    --block_size 8192 \
    --seed 42 \
    --pretrained_model_name_or_path $MODEL_PATH \
    --epochs $EPOCHS \
    --lr $LR \
    --ckpt_num $CKPT_NUM \
    --tensorboard_log_dir $LOG_DIR \
    --output_ckpt_dir $CKPT_DIR \
    --sft_data_dir $DATASET_DIR \
    --mode sft \
    --use_lora \
    --target_modules "q_proj, k_proj, v_proj" \
    --r 256 \
    --lora_alpha 512 \
    --lora_dropout 0.1

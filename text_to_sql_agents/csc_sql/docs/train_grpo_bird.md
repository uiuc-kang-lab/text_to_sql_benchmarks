# train nl2sql grpo bird

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

## download dataset 

### download bird dataset 

bird train and eval dataset 
```shell
mkdir -p ${HOME}/work/bird
cd ${HOME}/work/bird

# bird train
wget https://bird-bench.oss-cn-beijing.aliyuncs.com/train.zip
unzip train.zip
# bird dev
wget https://bird-bench.oss-cn-beijing.aliyuncs.com/dev.zip
unzip dev.zip
```

### download train bird grpo dataset 

from huggingface
```shell
mkdir -p ${HOME}/work/bird_train
huggingface-cli download cycloneboy/bird_train --repo-type dataset --local-dir ${HOME}/work/bird_train

```

or from modelscope
```shell
mkdir -p ${HOME}/work/bird_train
modelscope download --dataset  cycloneboy/bird_train --local_dir ${HOME}/work/bird_train

```

bird grpo dataset file description

```shell
# Original bird training and development sets directly obtained from the seeklhy/SynSQL-2.5M dataset (OmniSQL)
bird_train/train_bird.json
bird_train/dev_bird.json
# Dataset for sql generate grpo training organized from seeklhy/SynSQL-2.5M dataset  (OmniSQL)
bird_train/train_sql_generate_omnisql_bird.json
bird_train/dev_sql_generate_omnisql_bird.json
# Generated merged revision training set for bird
bird_train/train_merge_bird.json

```

## GRPO training 

### modify train config

Configuration file description
```shell
########################################
# start the vLLM server config
bin/nl2sql/vllm_run.sh

# GRPO for sql generate 7b model
bin/nl2sql/train_nl2sql_sql_generate_7b.sh
# GRPO for sql merge revision 7b model
bin/nl2sql/train_nl2sql_merge_7b.sh

# GRPO for sql generate 3b model
bin/nl2sql/train_nl2sql_sql_generate_3b.sh
# GRPO for sql merge revision 3b model
bin/nl2sql/train_nl2sql_merge_3b.sh

########################################
# accelerate deepspeed zero2 config
recipes/accelerate_configs/zero2.yaml

# GRPO for sql generate 7b model train config
recipes/Qwen2.5-Coder-7B-Instruct/grpo/config_sql_generate_rl.yaml

# GRPO for merge revision 7b model train config
recipes/Qwen2.5-Coder-7B-Instruct/grpo/config_merge_rl.yaml

# GRPO for sql generate 3b model train config
recipes/Qwen2.5-Coder-3B-Instruct/grpo/config_sql_generate_rl.yaml

# GRPO for merge revision 3b model train config
recipes/Qwen2.5-Coder-3B-Instruct/grpo/config_merge_rl.yaml

########################################
```

### demo for train sql generate 3b

> By default, vLLM downloads models from Hugging Face. If you would like to use models from ModelScope, set the environment variable VLLM_USE_MODELSCOPE before initializing the engine.
```shell
export VLLM_USE_MODELSCOPE=True
```

demo for train sql generate 3b
```shell
# modify model path and start vllm serve
bin/nl2sql/vllm_run.sh
# modify grpo train config 
vim recipes/Qwen2.5-Coder-3B-Instruct/grpo/config_sql_generate_rl.yaml
# check grpo train config path and start grpo train
bin/nl2sql/train_nl2sql_sql_generate_3b.sh

```

demo for train merge revision 3b
```shell
# modify model path and start vllm serve
bin/nl2sql/vllm_run.sh
# modify grpo train config 
vim recipes/Qwen2.5-Coder-3B-Instruct/grpo/config_merge_rl.yaml
# check grpo train config path and start grpo train
bin/nl2sql/train_nl2sql_merge_3b.sh

```

## grpo train code
```shell
# grpo train code
src/cscsql/service/grpo/nl2sql_grpo.py
# grpo reward code
src/cscsql/service/grpo/nl2sql_reward.py
```

## Thanks to the following projects
> The grpo training code can refer to open-r1

- [open-r1](https://github.com/huggingface/open-r1)
- [OmniSQL](https://github.com/RUCKBReasoning/OmniSQL)


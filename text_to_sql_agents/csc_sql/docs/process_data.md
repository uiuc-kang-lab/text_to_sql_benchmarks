# process data
> Our dataset processing work refers to OmniSQL
> https://github.com/RUCKBReasoning/OmniSQL/tree/main/train_and_evaluate


## download bird dataset 

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

## process dataset 


### Environment Setup
```shell
conda create -n cscsql_process_data python=3.9.5
conda activate cscsql_process_data

# install jdk-11
sudo apt-get update
sudo apt-get install -y openjdk-11-jdk

pip3 install func_timeout ijson sqlglot tqdm jsonlines modelscope pyserini==0.22.1 faiss-cpu torch==2.1.0 numpy==1.24.3 nltk==3.8.1
python -c "import nltk;nltk.download('punkt')"

# install vllm
pip install vllm==0.8.0

# install flash-attention
pip install packaging ninja
pip install flash-attn --no-build-isolation

# install current project
cd csc_sql
pip install -e .
```

### nltk dependencies

Downloaded directly：

```shell
python -c "import nltk;nltk.download('punkt')"
```

Or use the file that has been downloaded：

```shell
cd csc_sql
mkdir -p ~/nltk_data/tokenizers/
cp -r data/nltk/punkt.zip ~/nltk_data/tokenizers/ 
unzip ~/nltk_data/tokenizers/punkt.zip -d ~/nltk_data/tokenizers/

```


### process dataset

```shell
cd csc_sql
# Configuration in bin/process/process_data.sh
# Note: You need to modify the database path configuration in bin/process/process_data.sh! ! ! (You can directly modify the example ## for BIRD test)
# DATASET_BASE_DIR: Data set root path
# DATASET_MODE: Data mode: dev, test
# DATAFILE_PATH: Data file path
# DATASET_PATH: Database file path
# TABLES_PATH: Data table file
# SAVE_INDEX_PATH: Index file path generated in the middle
# PROMPT_OUTPUT_PATH: Output prompt file path

bash bin/process/process_data.sh
```



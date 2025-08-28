# OmniSQL Training and Evaluation

## Environment Setup
All experiments were conducted using:
- **Anaconda 3**
- **Python 3.9.5**
- **8 x NVIDIA A800 80GB GPUs**

**Note:** A single A800 80GB GPU is sufficient for inference and evaluation. For training OmniSQL from scratch, 8 x A800 80GB GPUs are recommended.

## Dataset Preparation

### Download
Download the datasets from:
- [ModelScope-OmniSQL-datasets](https://modelscope.cn/datasets/seeklhy/OmniSQL-datasets/summary)
- [HuggingFace-OmniSQL-datasets](https://huggingface.co/datasets/seeklhy/OmniSQL-datasets)

The datasets include BIRD, Spider, ScienceBenchmark, EHRSQL, Spider2-SQLite, Spider-DK, Spider-Realistic, Spider-Syn, and SynSQL-2.5M. Unzip `data.zip` in this folder.

### Pre-processing
The pre-processed datasets are included in `data.zip` (see the `*.json` files). You can also reproduce the pre-processing steps if needed.

1. **Set Up Environment:**
   ```sh
   conda create -n omnisql_process_data python=3.9.5
   conda activate omnisql_process_data

   apt-get update
   apt-get install -y openjdk-11-jdk
   
   pip3 install func_timeout ijson pyserini==0.22.1 faiss-cpu torch==2.1.0 numpy==1.24.3 nltk==3.8.1
   python3 nltk_downloader.py
   ```

2. **Run Pre-processing Scripts:**
   ```sh
   # Build BM25 index for database values
   python3 build_contents_index.py
   # Prepare input-output sequences
   sh process_dataset.sh
   ```

   **Note:** Processing SynSQL-2.5M may take over 24 hours due to its size (~2.5 million samples).

## Evaluation Reproduction
You can easily reproduce our evaluation results as follows:

1. **Set Up Environment:**
   ```sh
   conda create -n omnisql_eval python=3.9.5
   conda activate omnisql_eval
   pip3 install vllm==0.6.3.post1 func_timeout tqdm matplotlib nltk==3.8.1 sqlparse
   python3 nltk_downloader.py
   ```

2. **Download Evaluation Materials:**
   Download Spider's test-suite databases and evaluation scripts from [test_suite_sql_eval.zip](https://drive.google.com/file/d/1iNa1WgA9tN_OFna08nq_tHZdXx9Lz2vO/view) and unzip `test_suite_sql_eval.zip` in this folder.

3. **Run Evaluation:**
   ```python
   python3 eval_open_source_models.py
   ```
   Predicted SQL queries are saved in the `results` folder, and evaluation results (e.g., model accuracy) are stored in the `evaluation_results` folder.

## Training OmniSQL from Scratch
To train OmniSQL from scratch:

1. **Set Up Environment:**
   ```sh
   conda create -n omnisql_train python=3.9.5
   conda activate omnisql_train
   pip3 install torch==2.1.0 torchvision==0.16.0 torchaudio==2.1.0 transformers==4.45.1 accelerate==0.34.2 deepspeed==0.10.3 numpy==1.24.3 peft datasets tensorboard ijson
   ```

   To speed up attention calculation, install flash-attention:

   ```bash
   # Build from source (not recommended)
   pip3 install flash-attn==2.5.8 --no-build-isolation
   ```

   It's recommended to download a precompiled flash-attn Wheel from [flash-attn-2.5.8](https://github.com/Dao-AILab/flash-attention/releases/tag/v2.5.8). Choose the appropriate `.whl` file based on your environment: `flash_attn-2.5.8+cu{cuda_version}torch{torch_version}cxx11abiFALSE-cp{python_version}-cp{python_version}-linux_x86_64.whl`. 

   For example, if your CUDA version is 12.2, PyTorch version is 2.1, and Python version is 3.9.5, download `flash_attn-2.5.8+cu122torch2.1cxx11abiFALSE-cp39-cp39-linux_x86_64.whl` and install it using `pip3 install`.

2. **Training Scripts:**
   ```sh
   # train OmniSQL-7B using SynSQL-2.5M
   sh train_omnisql_7b.sh
   # train OmniSQL-14B using SynSQL-2.5M
   sh train_omnisql_14b.sh
   # train OmniSQL-32B using SynSQL-2.5M
   sh train_omnisql_32b.sh
   ```

   To train the full version of OmniSQL, you should manually merge the three training sets (`./data/train_synsql.json`, `./data/train_bird.json`, and `./data/train_spider.json`) and update the `DATASET_DIR` in the scripts. For OmniSQL-32B, you can merge LoRA adapters into the base model using `merge_lora_adapter.py`.

   **Note:** Training OmniSQL from scratch is resource and time-intensive. As reported in our paper, training OmniSQL-7B/14B/32B requires approximately 6, 12, and 20 days, respectively, on a single machine equipped with 8 NVIDIA A800 80GB GPUs. Please consider whether you need to train them again. **We encourage using our open-sourced OmniSQL models directly or continuing to train your text-to-SQL model with a smaller dataset based on OmniSQL.**
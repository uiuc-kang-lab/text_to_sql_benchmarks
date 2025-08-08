# ContextualAI's text-to-SQL pipeline for BIRD benchmark

<p align="center">
  &nbsp&nbsp🤗 <a href="https://huggingface.co/collections/ContextualAI/contextual-sql-68648806afcb0a708adbc4fb">Models</a>&nbsp&nbsp | &nbsp&nbsp :bookmark_tabs: <a href="https://qwenlm.github.io/blog/qwen3/">Blog</a>
</p>

## Environment Setup

Requires Python 3.10.
Install the required dependencies using the provided requirements file:

```bash
pip install -r requirements.txt
```

## Model Setup

Download the required models from HuggingFace to the `models/` directory:

### Generator Model

```bash
mkdir -p models/generator
hf download Qwen/Qwen2.5-Coder-32B-Instruct \
  --local-dir models/generator
```

### Reward Model

```bash
mkdir -p models/reward
hf download sheshansh-ctx/ctx-bird-reward-250121 \
  --local-dir models/reward
```

## Data Setup

Download and preprocess the BIRD benchmark dataset:

```bash
python src/prep_data.py
```

This will:
- Download the BIRD development dataset
- Extract and organize files in `data/` directory  
- Generate database schemas and processed JSONL output

## Execution

Requires 2+ GPUs with 80GB RAM each.
The pipeline consists of four main stages:

1. **Candidate Generation**: Generate multiple SQL query candidates
```bash
python src/generate.py --input_file data/test_all.jsonl --output_dir output/generations/ --num_gpus 2
```
2. **SQL execution**: Execute SQL candidates
```bash
python src/process_sqls.py --input_file data/test_all.jsonl --generations_dir output/generations/ --output_dir output/with_results/ --compare_against_gt --sql_timeout 30.0
```

> **Note**: The `--sql_timeout` parameter should be tuned based on your database performance and CPU capabilities. SQL queries that exceed the timeout are filtered in subsequent steps. For slower hardware, consider increasing the timeout value to avoid excessive query filtering.

> **Note**: The script is written such that SQL execution can be run in parallel with generation, and it waits on generation job to generate more candidates.

3. **Reward-Based Scoring**: Score candidates using the reward model
```bash
VLLM_USE_V1=0 time python src/reward.py --input_file output/with_results/data_with_results.jsonl --output_dir output/with_rewards --num_gpus 2
```

4. **Analysis**: Choose the highest-scoring SQL for final output
```bash
python src/analysis.py --rewards_dir output/with_rewards --gt_sql_file data/test_gold_sqls.txt --output_dir output/analysis --num_cpus 100
```

## Citation

```bibtex
@misc{agrawal2025text2sql,
  author       = {Sheshansh Agrawal and Thien Nguyen},
  title        = {Open-Sourcing the Best Local Text-to-SQL System},
  year         = {2025},
  url          = {https://contextual.ai/blog/open-sourcing-the-best-local-text-to-sql-system/}
}
```

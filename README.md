# Pervasive Annotation Errors Break Text-to-SQL Benchmarks and Leaderboards

This repository contains the code and data for the paper “Pervasive Annotation Errors Break Text-to-SQL Benchmarks and Leaderboards.”

We introduce SAR-Agent, the first AI agent for detecting annotation errors in text-to-SQL benchmarks via multi-turn interaction with the database. Using SAR-Agent and expert analysis, we find that BIRD Mini-Dev and Spider 2.0-Snow have error rates of 52.8% and 62.8%, respectively.

We corrected 100 examples sampled from the BIRD Dev set and re-evaluated all 16 open-source agents from the BIRD leaderboard. We observe performance changes of −7% to +31% (relative) and ranking changes from −9 to +9.

Execution accuracy of agents on original and corrected BIRD Dev subsets  
![Figure 1: Execution accuracy of agents on original and corrected BIRD Dev subsets.](materials/ex.png)

Agent ranking changes from original to corrected BIRD Dev subset  
![Figure 2: Agent ranking changes from original to corrected BIRD Dev subset.](materials/rank.png)

Repository layout
- SAR-Agent: implementation of SAR-Agent
- text_to_sql_agents: code and outputs for the 16 open-source agents we re-evaluated

## Quick start

- Reproduce SAR-Agent runs (OpenAI o3):
  1) Install dependencies
  2) Prepare databases (BIRD or Spider 2.0-Snow)
  3) Set your OpenAI API key
  4) Run SAR-Agent with the provided scripts/configs

- Reproduce agent re-evaluations:
  1) Download both the original and corrected BIRD Dev subsets
  2) Use the released agent outputs, or run agents as instructed in each agent’s folder
  3) Run the evaluation scripts to compute execution accuracy and rankings

## SAR-Agent

We used OpenAI’s o3 model in our experiments.

Prerequisites
- Python 3.9+
- pip or conda
- Access to the relevant databases (BIRD or Spider 2.0-Snow)

Install
```
cd SAR-Agent
pip install -r requirements.txt
```

Set credentials
- OpenAI:
    ```
    export OPENAI_API_KEY='<your_api_key>'
    ```

### Data setup

BIRD
- Download the BIRD Dev set and databases from the official BIRD repository or website.
- Place databases under, e.g., data/bird/databases
- Place the Dev split under, e.g., data/bird/dev/
- If using our corrected subset (100 examples), place it under, e.g., data/bird/dev/corrected/

Spider 2.0-Snow
- Request Snowflake access via the Spider 2.0 repository: https://github.com/xlang-ai/Spider2.git
- Configure Snowflake credentials.

Note: Replace placeholder paths with your actual locations. Ensure DB servers are reachable where applicable.

### Run SAR-Agent

Example invocations:
- BIRD:
  ```
  ```
- Spider 2.0-Snow:
  ```
  ```


## Re-evaluation of open-source agents

We include 16 open-source agents from the BIRD leaderboard under text_to_sql_agents. For convenience, we also include the generated SQL outputs used in our study.

### Data setup

- Download the original and corrected BIRD Dev subsets 

### Use released outputs

- Each agent folder under text_to_sql_agents contains a results/ subfolder with generated queries for both the original and corrected subsets (see each agent’s README for file names).
- To compute execution accuracy, run the evaluation script, for example:
  ```
  python evaluate.py 
  ```
  and for the corrected subset:
  ```
  python evaluate.py 
  ```

### Run agents yourself (optional)

- Each agent folder contains a README with environment setup, checkpoints, and run commands.
- You can follow their README files to run agents yourself.


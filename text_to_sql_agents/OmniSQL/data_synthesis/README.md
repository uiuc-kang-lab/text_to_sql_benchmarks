# Data Synthesis Framework

This directory contains the source code and prompts for our data synthesis framework.

- **Step 1:** Web Table-Driven Database Synthesis (see `database_synthesis`)
- **Step 2:** Complexity-Aware SQL Query Generation (see `sql_synthesis`)
- **Step 3:** Stylized Natural Language Question Synthesis (see `question_synthesis`)
- **Step 4:** Chain-of-Thought Solution Synthesis (see `cot_synthesis`)

These steps are sequential, but you can start at any intermediate step to synthesize text-to-SQL data samples. For instance, if you already have databases, you can skip Step 1 and generate high-quality `<question, SQL query, CoT solution>` pairs for your databases.

To set up the Anaconda environment for data synthesis:

```bash
conda create -n omnisql_data_synthesis python=3.9.5
conda activate omnisql_data_synthesis

pip install -U sentence-transformers
pip install json-repair ijson matplotlib func_timeout
```
# OpenSearch-SQL

一个完整的 Text-to-SQL 框架, 2024 年 8 月在[BIRD](https://bird-bench.github.io/)上取得第一名。下面是完整的流程图

<p align="center">
  <img src="./image/overview3.jpg" alt="image" />
</p>
<div align="center">
  
[📖 Arxiv](https://arxiv.org/abs/2502.14913) |
中文版 |
[EN](./readme.md)

</div>

## Text-to-SQL

Text-to-SQL 任务的目标是使从业人员不必掌握专门的数据库技能，它将用户的自然语言描述转化为 SQL 查询来完成用户的需求。比如：

**User Query**:

```
"What is the tallest building?"
```

**SQL Query**:

```sql
SELECT building_name FROM buildings ORDER BY height DESC LIMIT 1
```

## Overview

OpenSearch-SQL 通过 Preprocessing、Extraction、Generation、Refinement 以及 Alignment 模块组成。
整个 OpenSearch-SQL 框架运行不依赖于额外训练，你可以使用 GPT、DeepSeek、Gemini 等模型完成工作。

除了 Schemelinking、BeamSearch 采样生成答案和 Self-Consistnecy \& vote 之外，我们依赖独特的框架设计取得了效果的提升。

1. 在 OpenSearch-SQL 中，我们第一次提出了 Self-taught 的 CoT 补充方法，将 Query-SQL Pair 形式的 Few-shot 扩展成 Query-CoT-SQL Pair，这大大提升了模型表现。另外，我们发现，与query更相似的few-shot不一定对模型的表现更有帮助。希望这对你的研究有帮助
2. 我们为 Text-to-SQL 任务设计了一种结构化的 CoT 思路，并设计了 SQL-Like 的中间语言来优化 SQL 生成
3. 除此之外，我们第一次提出了 Alignment 方法，将 Agent 的输入输出进行对齐，这缓解了模型幻觉的问题。
   例如：不同数据集的风格要求、Agent 信息传递的幻觉、生成 SQL 的基本逻辑问题
4. 在提交时，我们在 BIRD 的三个榜单上都取得了第一：验证集上 69.3%的 EX，测试集上 72.28%的 EX，69.36%的 R-VES.
<p align="center">
  <img src="./image/bird_ranl.jpg" alt="image" />
</p>

# Run

**installation**：

```shell
pip install -r requirements.txt
```

**Data processing**：
更新 对于 few-shot，我们采用了[DAIL-SQL](https://github.com/BeachWang/DAIL-SQL)方法生成 few-shot 示例。你也可以选择其他方法创建 few-shot query-SQL 对。此外，你还可以直接使用我们提供的由'src/database_process/generate_question.py'生成的[questions](./Bird/fewshot/questions.json)。

最近，我们提供了使用 DAIL-SQL 获得的 few-shot 源文件['bird_dev.json'](./Bird/bird_dev.json)。你可以使用它运行'src/database_process/generate_question.py'。

```bash
sh run/run_preprocess.sh  # 每个目录的输出见控制台输出，处理fewshot，table 等数据
```

你也可以直接使用在 Bird 路径下的 fewshot

**Main**：

```bash
sh run/run_main.sh  # ，path：src/runner/database_manager.py-> _set_paths
```

## 8. Citation

```
@misc{xie2025opensearchsqlenhancingtexttosqldynamic,
      title={OpenSearch-SQL: Enhancing Text-to-SQL with Dynamic Few-shot and Consistency Alignment},
      author={Xiangjin Xie and Guangwei Xu and Lingyan Zhao and Ruijie Guo},
      year={2025},
      eprint={2502.14913},
      archivePrefix={arXiv},
      primaryClass={cs.CL},
      url={https://arxiv.org/abs/2502.14913},
}
```

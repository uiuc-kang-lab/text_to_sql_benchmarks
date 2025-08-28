#! /bin/bash

start_time=$(date +%s)

python -m alphasql.runner.mcts_runner config/qwen7b_sds_exp.yaml

end_time=$(date +%s)
echo "Time taken: $((end_time - start_time)) seconds"

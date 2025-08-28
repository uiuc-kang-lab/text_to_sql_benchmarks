#! /bin/bash

python -m alphasql.runner.preprocessor \
    --data_file_path "data/bird/dev/dev.json" \
    --database_root_dir "data/bird/dev/dev_databases" \
    --save_root_dir "data/preprocessed/bird/dev" \
    --lsh_threshold 0.5 \
    --lsh_signature_size 128 \
    --lsh_n_gram 3 \
    --lsh_top_k 20 \
    --edit_similarity_threshold 0.3 \
    --embedding_similarity_threshold 0.6 \
    --n_parallel_processes 8 \
    --max_dataset_samples -1
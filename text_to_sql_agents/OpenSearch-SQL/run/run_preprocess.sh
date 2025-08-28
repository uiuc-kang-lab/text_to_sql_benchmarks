db_root_directory=Bird #root directory
dev_json=dev/dev.json
train_json=train/train.json
dev_table=dev/dev_tables.json  # 11 dev data
train_table=train/train_tables.json  # 69 train data
dev_database=dev/dev_databases #dev database directory
fewshot_llm=gpt-4o-0513
DAIL_SQL=Bird/bird_dev.json     #dailsql json file 
bert_model=bge/ 

python -u src/database_process/data_preprocess.py \
    --db_root_directory "${db_root_directory}" \
    --dev_json "${dev_json}" \
    --train_json "${train_json}" \
    --dev_table "${dev_table}" \
    --train_table "${train_table}"


python -u src/database_process/prepare_train_queries.py \
    --db_root_directory "${db_root_directory}" \
    --model "${fewshot_llm}" 


python -u src/database_process/generate_question.py \
    --db_root_directory "${db_root_directory}" \
    --DAIL_SQL "${DAIL_SQL}" 


python -u src/database_process/make_emb.py \
    --db_root_directory "${db_root_directory}" \
    --dev_database "${dev_database}" \
    --bert_model "${bert_model}"

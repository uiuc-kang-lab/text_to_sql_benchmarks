set -e

# Spider (dev)
python process_dataset.py --input_data_file ./data/spider/dev.json --output_data_file ./data/dev_spider.json --db_path ./data/spider/database/ --tables ./data/spider/tables.json --source spider --mode dev --value_limit_num 2 --db_content_index_path ./data/spider/db_contents_index

# Spider (test)
python process_dataset.py --input_data_file ./data/spider/test.json --output_data_file ./data/test_spider.json --db_path ./data/spider/test_database/ --tables ./data/spider/test_tables.json --source spider --mode test --value_limit_num 2 --db_content_index_path ./data/spider/db_contents_index

# BIRD (dev)
python process_dataset.py --input_data_file ./data/bird/dev_20240627/dev.json --output_data_file ./data/dev_bird.json --db_path ./data/bird/dev_20240627/dev_databases/ --tables ./data/bird/dev_20240627/dev_tables.json --source bird --mode dev --value_limit_num 2 --db_content_index_path ./data/bird/dev_20240627/db_contents_index

# Spider2.0-SQLite
python process_dataset.py --input_data_file ./data/spider2_sqlite/test.json --output_data_file ./data/test_spider2_sqlite.json --db_path ./data/spider2_sqlite/databases/ --tables ./data/spider2_sqlite/tables.json --source spider2.0 --mode test --value_limit_num 2 --db_content_index_path ./data/spider2_sqlite/db_contents_index

# Spider-DK
python process_dataset.py --input_data_file ./data/Spider-DK/Spider-DK.json --output_data_file ./data/dev_spider_dk.json --db_path ./data/Spider-DK/database --tables ./data/Spider-DK/tables.json --source spider_dk --mode dev --value_limit_num 2 --db_content_index_path ./data/Spider-DK/db_contents_index

# Spider-Realistic
python process_dataset.py --input_data_file ./data/spider-realistic/spider-realistic.json --output_data_file ./data/dev_spider_realistic.json --db_path ./data/spider/database/ --tables ./data/spider/tables.json --source spider_realistic --mode dev --value_limit_num 2 --db_content_index_path ./data/spider/db_contents_index

# Spider-Syn
python process_dataset.py --input_data_file ./data/Spider-Syn/dev.json --output_data_file ./data/dev_spider_syn.json --db_path ./data/spider/database/ --tables ./data/spider/tables.json --source spider_syn --mode dev --value_limit_num 2 --db_content_index_path ./data/spider/db_contents_index

# EHRSQL
python process_dataset.py --input_data_file ./data/EHRSQL/dev.json --output_data_file ./data/dev_ehrsql.json --db_path ./data/EHRSQL/database --tables ./data/EHRSQL/tables.json --source ehrsql --mode dev --value_limit_num 2 --db_content_index_path ./data/EHRSQL/db_contents_index

# ScienceBenchmark
python process_dataset.py --input_data_file ./data/sciencebenchmark/dev.json --output_data_file ./data/dev_sciencebenchmark.json --db_path ./data/sciencebenchmark/databases --tables ./data/sciencebenchmark/tables.json --source sciencebenchmark --mode dev --value_limit_num 2 --db_content_index_path ./data/sciencebenchmark/db_contents_index

# Spider (Training set)
python process_dataset.py --input_data_file ./data/spider/train_spider_enhanced_with_cot.json --output_data_file ./data/train_spider.json --db_path ./data/spider/database/ --tables ./data/spider/tables.json --source spider --mode train --value_limit_num 2 --db_content_index_path ./data/spider/db_contents_index

# BIRD (Training set)
python process_dataset.py --input_data_file ./data/bird/train/train_enhanced_with_cot.json --output_data_file ./data/train_bird.json --db_path ./data/bird/train/train_databases/ --tables ./data/bird/train/train_tables.json --source bird --mode train --value_limit_num 2 --db_content_index_path ./data/bird/train/db_contents_index

# SynSQL-2.5M
python process_dataset.py --input_data_file ./data/SynSQL-2.5M/data.json --output_data_file ./data/train_synsql.json --db_path ./data/SynSQL-2.5M/databases --tables ./data/SynSQL-2.5M/tables.json --source synthetic --mode train --value_limit_num 2 --db_content_index_path ./data/SynSQL-2.5M/db_contents_index

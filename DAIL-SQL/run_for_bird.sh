python data_preprocess.py --data_type bird --data_dir ./dataset/bird

# Method 1
python generate_question.py --data_type bird \
--split test --tokenizer gpt-4o --prompt_repr SQL \
--selector_type EUCDISQUESTIONMASK --max_seq_len 4096 --k_shot 7 --example_type QA

python ask_llm.py \
--model gpt-4o \
--question ./dataset/process/BIRD-TEST_SQL_7-SHOT_EUCDISQUESTIONMASK_QA-EXAMPLE_CTX-200_ANS-4096/ \
--db_dir ./dataset/bird/databases


# Method 2
python generate_question.py --data_type bird --split test --tokenizer gpt-4o \
--prompt_repr SQL --max_seq_len 4096 --k_shot 7 --example_type QA --selector_type EUCDISMASKPRESKLSIMTHR \
--pre_test_result ./dataset/process/BIRD-TEST_SQL_7-SHOT_EUCDISQUESTIONMASK_QA-EXAMPLE_CTX-200_ANS-4096/RESULTS_MODEL-gpt-4o.txt

python ask_llm.py \
--model gpt-4o \
--question ./dataset/process/BIRD-TEST_SQL_7-SHOT_EUCDISMASKPRESKLSIMTHR_QA-EXAMPLE_CTX-200_ANS-4096/ \
--db_dir ./dataset/bird/databases


# Result
python to_bird_output.py --dail_output ./dataset/process/BIRD-TEST_SQL_7-SHOT_EUCDISMASKPRESKLSIMTHR_QA-EXAMPLE_CTX-200_ANS-4096/RESULTS_MODEL-gpt-4o.txt

cp ./dataset/process/BIRD-TEST_SQL_7-SHOT_EUCDISMASKPRESKLSIMTHR_QA-EXAMPLE_CTX-200_ANS-4096/RESULTS_MODEL-gpt-4o.json ./RESULTS_MODEL-gpt-4o.json

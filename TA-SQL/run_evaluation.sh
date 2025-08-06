db_root_path='./data/dev_databases/'
data_mode='dev'
diff_json_path='./data/dev_databases/dev.json'
predicted_sql_path_kg='./outputs/'
ground_truth_path='./data/dev_databases/'
num_cpus=16
meta_time_out=30.0
mode_gt='gt'
mode_predict='gpt'

echo '''starting to compare with knowledge for ex and ves'''
python3 -u ./evaluation/evaluation.py --db_root_path ${db_root_path} --predicted_sql_path ${predicted_sql_path_kg} --data_mode ${data_mode} \
--ground_truth_path ${ground_truth_path} --num_cpus ${num_cpus} --mode_gt ${mode_gt} --mode_predict ${mode_predict} \
--diff_json_path ${diff_json_path} --meta_time_out ${meta_time_out} 

python3 -u ./evaluation/evaluation_ves.py --db_root_path ${db_root_path} --predicted_sql_path ${predicted_sql_path_kg} --data_mode ${data_mode} \
--ground_truth_path ${ground_truth_path} --num_cpus ${num_cpus} --mode_gt ${mode_gt} --mode_predict ${mode_predict} \
--diff_json_path ${diff_json_path} --meta_time_out ${meta_time_out} 
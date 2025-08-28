# Define variables
data_mode='dev' # Options: 'dev', 'train' 
db_root_path=Bird #root directory # UPDATE THIS WITH THE PATH TO THE TARGET DATASET
start=0 #闭区间
end=1  #开区间
pipeline_nodes='generate_db_schema+extract_col_value+extract_query_noun+column_retrieve_and_other_info+candidate_generate+align_correct+vote+evaluation'
# pipeline_nodes='column_retrieve_and_other_info'
# pipeline指当前工作流的节点组合
# checkpoint_nodes='generate_db_schema,extract_col_value,extract_query_noun'
# checkpoint_dir="./results/dev/generate_db_schema+extract_col_value+extract_query_noun+column_retrieve_and_other_info+candidate_generate+align_correct+vote+evaluation/Bird/2024-09-12-01-48-10"

# Nodes:
    # generate_db_schema
    # extract_col_value
    # extract_query_noun
    # column_retrieve_and_other_info
    # candidate_generate
    # align_correct
    # vote
    # evaluation

AK='your_ak' #set your ak in src/llm/model.py
engine1='gpt-4o-0513'
engine2='gpt-3.5-turbo-0125'
engine3='gpt-4-turbo'
engine4='claude-3-opus-20240229'
engine5='gemini-1.5-pro-latest'
engine6='finetuned_nl2sql'
engine7='meta-llama/Meta-Llama-3-70B-Instruct'
engine8='finetuned_colsel'
engine9='finetuned_col_filter'
engine10='gpt-3.5-turbo-instruct'

## n默认21 
#align_methods:style_align+function_align+agent_align
#暂时没有找到好的注释方式
# pipeline_setup='{
#     "generate_db_schema": {                 #生成db_schema的环节
#         "engine": "'${engine1}'",            #生成 db_schema的大模型选择                 
#         "bert_model": "/app/sentence-transformers/all-mpnet-base-v2/",  #bert_model模型选择
#         "device":"cpu"                                                  #bert_model加载方式，目前该机器只支持cpu
#     },
#     "extract_col_value": {                    #get_des_ans得到key_col_des_raw
#         "engine": "'${engine1}'",             #大模型
#         "temperature":0.0                     #大模型的生成参数选择
#     },
#     "extract_query_noun": {                   #parse_des得到col和value
#         "engine": "'${engine1}'",             #parse_des使用的大模型
#         "temperature":0.0                     #大模型的生成参数选择
#     },
#     "column_retrieve_and_other_info": {      #得到一些列描述和列等相关信息+query_order
#         "engine": "'${engine1}'",             #query_order用的大模型
#         "bert_model": "/app/bge",        # bert_model模型选择
#         "device":"cpu",                          #bert_model加载方式，目前该机器只支持cpu
#         "temperature":0.3,                        #query_order使用大模型的生成参数
#         "top_k":10                                #get_key_col_des里面的top_k
#     },
#     "candidate_generate":{                    #生成候选sql
#         "engine": "'${engine1}'",             #大模型
#         "temperature": 0.7,                   #大模型的参数
#         "n":21,                               #n，同align环节n一致
#         "return_question":"True",             #get_sql里的参数
#         "single":"False"                      #get_sql里的参数，n=1时和n！=1处理方式有差异
#     },
#     "align_correct":{
#         "engine": "'${engine1}'",             #对齐和纠错
#         "n":21,                                  #多线程的数量
#         "bert_model": "/app/bge",            
#         "device":"cpu",                           #bert_model 加载方式
#         "align_methods":"style_align+function_align+agent_align"   #对齐方式，以+号分割
#     }
# }'  
pipeline_setup='{
    "generate_db_schema": {
        "engine": "'${engine1}'",
        "bert_model": "your_bert_model_path",  
        "device":"cpu"
    },
    "extract_col_value": {
        "engine": "'${engine1}'",
        "temperature":0.0
    },
    "extract_query_noun": {
        "engine": "'${engine1}'",
        "temperature":0.0
    },
    "column_retrieve_and_other_info": {
        "engine": "'${engine1}'",
        "bert_model": "your_bert_model_path",  
        "device":"cpu",
        "temperature":0.3,
        "top_k":10
    },
    "candidate_generate":{
        "engine": "'${engine1}'",
        "temperature": 0.7,  
        "n":21,
        "return_question":"True",
        "single":"False"
    },
    "align_correct":{
        "engine": "'${engine1}'",
        "n":21,
        "bert_model": "your_bert_model_path:e.g. /opensearch-sql/bge",  
        "device":"cpu",
        "align_methods":"style_align+function_align+agent_align"
    }
}'  

python3 -u ./src/main.py --data_mode ${data_mode} --db_root_path ${db_root_path}\
        --pipeline_nodes ${pipeline_nodes} --pipeline_setup "$pipeline_setup"\
        --start ${start} --end ${end} \
        # --use_checkpoint --checkpoint_nodes ${checkpoint_nodes} --checkpoint_dir ${checkpoint_dir}
  

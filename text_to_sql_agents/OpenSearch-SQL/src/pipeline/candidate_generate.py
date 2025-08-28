import logging
from typing import Any, Dict, List
from pipeline.utils import node_decorator,get_last_node_result
from pipeline.pipeline_manager import PipelineManager
from runner.database_manager import DatabaseManager
from pipeline.utils import make_newprompt
from llm.model import model_chose
from llm.db_conclusion import *
import json
from llm.prompts import *
from runner.check_and_correct import get_sql

@node_decorator(check_schema_status=False)
def candidate_generate(task: Any, execution_history: List[Dict[str, Any]]) -> Dict[str, Any]:
    config,node_name=PipelineManager().get_model_para()
    paths=DatabaseManager()
    fewshot_path=paths.db_fewshot_path

    with open(fewshot_path) as f:## fewshot
        df_fewshot = json.load(f)

    chat_model = model_chose(node_name,config["engine"])  # deepseek qwen-max gpt qwen-max-longcontext
    column = get_last_node_result(execution_history, "column_retrieve_and_other_info")["column"]
    foreign_keys= get_last_node_result(execution_history, "column_retrieve_and_other_info")["foreign_keys"]
    L_values = get_last_node_result(execution_history, "column_retrieve_and_other_info")["L_values"]
    q_order = get_last_node_result(execution_history, "column_retrieve_and_other_info")["q_order"]
    values = [f"{x[0]}: '{x[1]}'" for x in L_values]
    db=task.db_id

    key_col_des = "#Values in Database:\n" + '\n'.join(values)
    # key_col_des = ""
    
    new_db_info = f"Database Management System: SQLite\n#Database name: {db} \n{column}\n\n#Forigen keys:\n{foreign_keys}\n"
    # new_db_info=get_last_node_result(execution_history, "generate_db_schema")["db_list"]

    # question=rewrite_question(task.question)
    question=task.question
    fewshot=df_fewshot["questions"][task.question_id]['prompt']
    # fewshot=""
    # fewshot=fewshot.split("\n/* Given the following database schema: */")[0]
    new_prompt = make_newprompt(db_check_prompts().new_prompt, fewshot,
                            key_col_des, new_db_info, question,
                            task.evidence,q_order)

    single = config['single'].lower() == 'true'  # 将字符串转换为布尔值
    return_question=config['return_question']== 'true' 
    SQL,_ = get_sql(chat_model, new_prompt, config['temperature'], return_question=return_question,n=config['n'],single=single)

    
    response = {
        "rewrite_question":question,
        "SQL": SQL
        # "new_prompt":new_prompt
    }

    return response




def rewrite_question(question):
    if question.find(" / ")!=-1:
        question+=". For division operations, use CAST xxx AS REAL to ensure precise decimal results"
    return question

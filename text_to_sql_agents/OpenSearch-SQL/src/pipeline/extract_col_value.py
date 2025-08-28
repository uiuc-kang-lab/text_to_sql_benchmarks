import logging
from typing import Any, Dict
from pathlib import Path
from pipeline.utils import node_decorator,get_last_node_result
from pipeline.pipeline_manager import PipelineManager
from runner.database_manager import DatabaseManager
from llm.model import model_chose
import json
from llm.prompts import *


@node_decorator(check_schema_status=False)
def extract_col_value(task: Any, execution_history: Dict[str, Any]) -> Dict[str, Any]:
    config,node_name=PipelineManager().get_model_para()
    paths=DatabaseManager()
    fewshot_path=paths.db_fewshot_path
    chat_model = model_chose(node_name,config["engine"])

    with open(fewshot_path) as f:## fewshot
        df_fewshot = json.load(f)

    hint = task.evidence
    if hint == "":
        hint = "None"
    

    all_info = get_last_node_result(execution_history, "generate_db_schema")["db_list"]
    key_col_des_raw = get_des_ans(chat_model,
                                db_check_prompts().extract_prompt,
                                df_fewshot["extract"][task.question_id]['prompt'],
                                all_info,
                                task.question,
                                hint,
                                False,
                                temperature=config["temperature"])

    response = {
        "key_col_des_raw": key_col_des_raw
    }
    return response

def get_des_ans(chat_model,
                ext_prompt,
                fewshot,
                db,
                question,
                hint,
                debug,
                temperature=1.0):
    fewshot = fewshot.split("/* Answer the following:")[1:6]
    fewshot = "/* Answer the following:" + "/* Answer the following:".join(
        fewshot)
    ext_prompt = ext_prompt.format(fewshot=fewshot,
                                   db_info=db,
                                   query=question,
                                   hint=hint)

    if debug:
        print(ext_prompt)
    pre_col_values = chat_model.get_ans(ext_prompt, temperature,
                                        debug=debug).replace('```', '')

    return pre_col_values



import logging,re
from typing import Any, Dict
from pathlib import Path
from pipeline.utils import node_decorator,get_last_node_result
from pipeline.pipeline_manager import PipelineManager
from llm.model import model_chose
from llm.prompts import *

@node_decorator(check_schema_status=False)
def extract_query_noun(task: Any,execution_history: Dict[str, Any]) -> Dict[str, Any]:
    config,node_name=PipelineManager().get_model_para()

    chat_model = model_chose(node_name,config["engine"])
    key_col_des_raw = get_last_node_result(execution_history, "extract_col_value")["key_col_des_raw"]
    noun_ext = chat_model.get_ans(db_check_prompts().noun_prompt.format(raw_question=task.question),temperature=config["temperature"])
    values, col = parse_des(key_col_des_raw, noun_ext, debug=False)
    
    response = {
        "values":values,
        "col":col
    }
    return response

def parse_des(pre_col_values, nouns, debug):
    pre_col_values = pre_col_values.split("/*")[0].strip()
    if debug:
        print(pre_col_values)
    col, values = pre_col_values.split('#values:')
    _, col = col.split("#columns:")
    col = strip_char(col)
    values = strip_char(values)

    if values == '':
        values = []
    else:
        values = re.findall(r"([\"'])(.*?)\1", values)
    nouns_all = re.findall(r"([\"'])(.*?)\1", nouns)
    values_noun = set(values).union(set(nouns_all))
    values_noun = [x[1] for x in values_noun]
    return values_noun, col


def strip_char(s):
    return s.strip('\n {}[]')
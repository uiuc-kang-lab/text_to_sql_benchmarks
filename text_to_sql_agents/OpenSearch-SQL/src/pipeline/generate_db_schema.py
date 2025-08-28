import logging
from typing import Any, Dict
from pathlib import Path
from sentence_transformers import SentenceTransformer
from pipeline.utils import node_decorator
from pipeline.pipeline_manager import PipelineManager
from runner.database_manager import DatabaseManager
from llm.model import model_chose
from llm.db_conclusion import *
import json

@node_decorator(check_schema_status=False)
def generate_db_schema(task: Any, execution_history: Dict[str, Any]) -> Dict[str, Any]:
    config,node_name=PipelineManager().get_model_para()
    paths=DatabaseManager()
    # 初始化模型
    bert_model = SentenceTransformer(config["bert_model"], device=config["device"])

    # 读取参数
    db_json_dir = paths.db_json
    tables_info_dir = paths.db_tables
    sqllite_dir=paths.db_path
    db_dir=paths.db_directory_path
    chat_model = model_chose(node_name,config["engine"])  # deepseek qwen-max gpt qwen-max-longcontext
    ext_file = Path(paths.db_root_path)/"db_schema.json"

    # 读取已有数据
    if os.path.exists(ext_file):
        with open(ext_file, 'r') as f:
            data = json.load(f)#保存格式错了
    else:
        data ={}

    # 获取数据库信息代理
    DB_info_agent = db_agent_string(chat_model)
    
    # 检查是否已处理该数据库
    db = task.db_id
    existing_entry = data.get(db)

    if existing_entry:
        all_info,db_col = existing_entry
    else:
        all_info, db_col = DB_info_agent.get_allinfo(db_json_dir, db,sqllite_dir,db_dir,tables_info_dir, bert_model)
        data[db]=[all_info,db_col]
        with open(ext_file, 'w') as f:
            json.dump(data, f, indent=4,ensure_ascii=False)
    
    response = {
        "db_list": all_info,
        "db_col_dic": db_col
    }
    return response





from functools import wraps
from typing import Dict, List, Any, Callable
from runner.logger import Logger
from runner.database_manager import DatabaseManager

def node_decorator(check_schema_status: bool = False) -> Callable:
    """
    A decorator to add logging and error handling to pipeline node functions.

    Args:
        check_schema_status (bool, optional): Whether to check the schema status. Defaults to False.

    Returns:
        Callable: The decorated function.
    """
    def decorator(func: Callable) -> Callable:
        @wraps(func)
        def wrapper(state: Dict[str, Any]) -> Dict[str, Any]:
            node_name = func.__name__
            Logger().log(f"---{node_name.upper()}---")
            result = {"node_type": node_name}

            try:
                task = state["keys"]["task"]
                execution_history = state["keys"]["execution_history"]
                for x in execution_history:
                    if x["node_type"]==node_name:
                        return state
                output = func(task,execution_history)
                result.update(output)
                result["status"] = "success"
            except Exception as e:
                Logger().log(f"Node '{node_name}': {task.db_id}_{task.question_id}\n{type(e)}: {e}\n", "error")
                # Logger().log(f"Vote content: {vote}, Type: {type(vote)}", "error")  # 打印 vote 内容
                result.update({
                    "status": "error",
                    "error": f"{type(e)}: <{e}>",
                })
            
            execution_history.append(result)
            # if execution_history[-1]["node_type"]=="align_correct":
            #     print(execution_history)
            Logger().dump_history_to_file(execution_history)
            
            return state
        return wrapper
    return decorator

def get_last_node_result(execution_history: List[Dict[str, Any]], node_type: str) -> Dict[str, Any]:
    """
    Retrieves the last result for a specific node type from the execution history.

    Args:
        execution_history (List[Dict[str, Any]]): The execution history.
        node_type (str): The type of node to look for.

    Returns:
        Dict[str, Any]: The result of the last node of the specified type, or None if not found.
    """
    for node in reversed(execution_history):
        if node["node_type"] == node_type:
            return node
    return None
            
def make_newprompt(new_prompt,
                   fewshot,
                   key_col_des,
                   db_info,
                   question,
                   hint="",q_order=""):
    n_prompt = new_prompt.format(fewshot=fewshot,
                                 db_info=db_info,
                                 question=question,
                                 hint=hint,
                                 key_col_des=key_col_des,q_order=q_order)

    return n_prompt

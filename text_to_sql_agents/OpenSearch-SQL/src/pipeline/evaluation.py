import logging
from typing import Dict, Any

from runner.logger import Logger
from runner.database_manager import DatabaseManager
from pipeline.utils import node_decorator, get_last_node_result
from runner.check_and_correct import sql_raw_parse

@node_decorator(check_schema_status=False)
def evaluation(task: Any, execution_history: Dict[str, Any]) -> Dict[str, Any]:
    """
    Evaluates the predicted SQL queries against the ground truth SQL query.

    Args:
        task (Any): The task object containing the question and evidence.
        tentative_schema (Dict[str, Any]): The current tentative schema.
        execution_history (Dict[str, Any]): The history of executions.

    Returns:
        Dict[str, Any]: A dictionary containing the evaluation results.
    """
    # logging.info("Starting evaluation")

    ground_truth_sql = task.SQL
    to_evaluate = {
        "candidate_generate": get_last_node_result(execution_history, "candidate_generate"), 
        "align_correct": get_last_node_result(execution_history, "align_correct"),#align+纠错 
        # "align": get_last_node_result(execution_history, "vote"), #未纠错
        # "correct":get_last_node_result(execution_history, "vote"),
        "vote": get_last_node_result(execution_history, "vote")
    }
    result = {}
    for evaluation_for, node_result in to_evaluate.items():
        predicted_sql = "--"
        evaluation_result = {}

        try:
            if node_result["status"] == "success":

                if evaluation_for =="align" :
                    predicted_sql=node_result['SQL_align_vote']
                elif evaluation_for =="correct" :
                    predicted_sql=node_result["SQL_correct_vote"]
                elif evaluation_for =="align_correct":
                    vote_all=node_result['vote']
                    predicted_sql=vote_all[0]['sql']
                elif evaluation_for=="candidate_generate":
                    candidate_all=node_result['SQL']
                    predicted_sql=sql_raw_parse(candidate_all[0], False)[0]
                elif evaluation_for=="vote":
                    predicted_sql = node_result["SQL"]
                response = DatabaseManager().compare_sqls(
                    predicted_sql=predicted_sql,
                    ground_truth_sql=ground_truth_sql,
                    meta_time_out=180
                )

                evaluation_result.update({
                    "exec_res": response["exec_res"],
                    "exec_err": response["exec_err"],
                })
            else:
                evaluation_result.update({
                    "exec_res": "generation error",
                    "exec_err": node_result["error"],
                })
        except Exception as e:
            Logger().log(
                f"Node 'evaluate_sql': {task.db_id}_{task.question_id}\n{type(e)}: {e}\n",
                "error",
            )
            evaluation_result.update({
                "exec_res": "error",
                "exec_err": str(e),
            })

        evaluation_result.update({
            "Question": task.raw_question,
            "Evidence": task.evidence,
            "GOLD_SQL": ground_truth_sql,
            "PREDICTED_SQL": predicted_sql
        })
        result[evaluation_for] = evaluation_result

    logging.info("Evaluation completed successfully")
    return result

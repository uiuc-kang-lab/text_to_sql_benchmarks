from alphasql.algorithm.mcts.mcts_node import MCTSNode, MCTSNodeType
from alphasql.algorithm.mcts.mcts_action import SQLGenerationAction, SQLRevisionAction
from alphasql.database.sql_execution import cached_execute_sql_with_timeout, SQLExecutionResultType, is_valid_execution_result
from typing import Dict, Any, List
from collections import defaultdict
from pathlib import Path

class RewardModel:
    def __init__(self, **kwargs):
        pass
    
    def get_reward(self, end_node: MCTSNode) -> float:
        pass

class MajorityVoteRewardModel(RewardModel):
    def __init__(self, llm_kwargs: Dict[str, Any]):
        self.llm_kwargs = llm_kwargs
        
    def get_reward(self, end_node: MCTSNode) -> float:
        assert end_node.node_type == MCTSNodeType.END
        parent_node = end_node.parent_node
        assert parent_node.node_type == MCTSNodeType.SQL_REVISION or parent_node.node_type == MCTSNodeType.SQL_GENERATION
        action = parent_node.parent_action
        assert isinstance(action, SQLGenerationAction) or isinstance(action, SQLRevisionAction)
        assert parent_node.parent_node is not None
        return end_node.consistency_score
        
    # def get_reward(self, end_node: MCTSNode) -> float:
    #     assert end_node.node_type == MCTSNodeType.END
    #     parent_node = end_node.parent_node
    #     assert parent_node.node_type == MCTSNodeType.SQL_REVISION or parent_node.node_type == MCTSNodeType.SQL_GENERATION
    #     action = parent_node.parent_action
    #     assert isinstance(action, SQLGenerationAction) or isinstance(action, SQLRevisionAction)
    #     assert parent_node.parent_node is not None
    #     end_sql_query = end_node.final_sql_query
    #     assert end_sql_query is not None
    #     if isinstance(action, SQLGenerationAction):
    #         return self.get_reward_for_sql_generation(parent_node.parent_node, end_sql_query)
    #     elif isinstance(action, SQLRevisionAction):
    #         return self.get_reward_for_sql_revision(parent_node.parent_node, end_sql_query)
    #     else:
    #         raise ValueError(f"Unknown action type: {type(action)}")
    
    # def majority_vote_confidence(self, sql_queries: List[str], end_sql_query: str, db_path: str) -> float:
    #     result_groups = defaultdict(list)
        
    #     end_sql_query_execution_result = cached_execute_sql_with_timeout(db_path, end_sql_query)
    #     if not is_valid_execution_result(end_sql_query_execution_result):
    #         return 0
        
    #     for sql_query in sql_queries:
    #         sql_query_execution_result = cached_execute_sql_with_timeout(db_path, sql_query)
    #         if not is_valid_execution_result(sql_query_execution_result):
    #             continue
    #         result_groups[frozenset(sql_query_execution_result.result)].append(sql_query)
            
    #     if len(result_groups) == 0:
    #         return 0
        
    #     same_with_end_sql_query_group_size = len(result_groups.get(frozenset(end_sql_query_execution_result.result), []))
    #     return same_with_end_sql_query_group_size / len(sql_queries)
    
    # def get_reward_for_sql_generation(self, node: MCTSNode, end_sql_query: str) -> float:
    #     action = SQLGenerationAction()
    #     children_nodes = action.create_children_nodes_without_self_consistency(node, llm_kwargs=self.llm_kwargs)
    #     assert len(children_nodes) > 0
    #     new_sql_queries = [child_node.sql_query for child_node in children_nodes]
    #     db_path = Path(node.db_root_dir) / node.db_id / f"{node.db_id}.sqlite"
    #     majority_vote_confidence = self.majority_vote_confidence(new_sql_queries, end_sql_query, db_path)
    #     return majority_vote_confidence
    
    # def get_reward_for_sql_revision(self, node: MCTSNode, end_sql_query: str) -> float:
    #     action = SQLRevisionAction()
    #     children_nodes = action.create_children_nodes_without_self_consistency(node, llm_kwargs=self.llm_kwargs)
    #     assert len(children_nodes) > 0
    #     new_sql_queries = [child_node.revised_sql_query for child_node in children_nodes]
    #     db_path = Path(node.db_root_dir) / node.db_id / f"{node.db_id}.sqlite"
    #     majority_vote_confidence = self.majority_vote_confidence(new_sql_queries, end_sql_query, db_path)
    #     return majority_vote_confidence

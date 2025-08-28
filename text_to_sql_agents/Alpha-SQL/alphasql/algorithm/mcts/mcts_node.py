from typing import List, Optional, Dict, Any
from alphasql.algorithm.mcts.mcts_action import *

def get_valid_action_space_for_node(node: "MCTSNode") -> List["MCTSAction"]:
    action_space_classes = NODE_TYPE_TO_VALID_ACTIONS[node.node_type]
    # if node.node_type == MCTSNodeType.SQL_GENERATION and node.is_valid_sql_query:
    #     action_space_classes = [action_class for action_class in action_space_classes if action_class.__name__ != "SQLRevisionAction"]
    history_actions_classes = [path_node.parent_action.__class__ for path_node in node.path_nodes if path_node.parent_action is not None]
    valid_action_space = [action_class() for action_class in action_space_classes if action_class not in history_actions_classes]
    return valid_action_space

class MCTSNode:
    def __init__(self,
                 node_type: "MCTSNodeType",
                 parent_node: Optional["MCTSNode"] = None,
                 parent_action: Optional["MCTSAction"] = None,
                 depth: int = 0,
                 db_id: str = "",
                 db_root_dir: str = "",
                 original_question: str = "",
                 hint: str = "",
                 schema_context: str = "",
                 table_schema_dict: Optional[Dict[str, "TableSchema"]] = None,
                 path_nodes: List["MCTSNode"] = [],
                 rephrased_question: Optional[str] = None,
                 selected_schema_dict: Optional[Dict[str, "TableSchema"]] = None,
                 selected_schema_context: Optional[str] = None,
                 identified_column_values: Optional[str] = None,
                 identified_column_functions: Optional[str] = None,
                 sql_query: Optional[str] = None,
                 revised_sql_query: Optional[str] = None,
                 final_sql_query: Optional[str] = None,
                 consistency_score: Optional[float] = None,
                 is_valid_sql_query: Optional[bool] = None,
                 llm_kwargs: Optional[Dict[str, Any]] = None
                 ):
        self.node_type = node_type
        self.parent_node = parent_node
        self.parent_action = parent_action
        self.depth = depth
        self.db_id = db_id
        self.db_root_dir = db_root_dir
        self.original_question = original_question
        self.hint = hint
        self.schema_context = schema_context
        self.table_schema_dict = table_schema_dict
        self.children : List[MCTSNode] = []
        self.path_nodes = path_nodes
        
        self.rephrased_question = rephrased_question
        self.selected_schema_dict = selected_schema_dict
        self.selected_schema_context = selected_schema_context
        self.identified_column_values = identified_column_values
        self.identified_column_functions = identified_column_functions
        self.sql_query = sql_query
        self.revised_sql_query = revised_sql_query
        self.final_sql_query = final_sql_query
        self.consistency_score = consistency_score
        self.is_valid_sql_query = is_valid_sql_query
        self.llm_kwargs = llm_kwargs

        self.Q = 0
        self.N = 0
    
    def create_children(self):
        if self.children:
            return
        
        valid_action_space = get_valid_action_space_for_node(self)
        for action in valid_action_space:
            self.children.extend(action.create_children_nodes(self, self.llm_kwargs))
            
    def is_terminal(self):
        return self.node_type == MCTSNodeType.END



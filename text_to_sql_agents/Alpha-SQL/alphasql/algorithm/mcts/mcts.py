from alphasql.algorithm.mcts.mcts_node import *
from alphasql.algorithm.mcts.mcts_action import *
from alphasql.algorithm.mcts.reward import *
from alphasql.runner.task import Task
import math
import random
from pathlib import Path
from typing import Dict, Any, List
import pickle

class MCTSSolver:
    def __init__(self,
                 db_root_dir: str,
                 task: Task, 
                 max_rollout_steps: int,
                 max_depth: int,
                 exploration_constant: float,
                 save_root_dir: str,
                 llm_kwargs: Dict[str, Any],
                 reward_model: RewardModel):
        self.llm_kwargs = llm_kwargs
        self.reward_model = reward_model
        self.task = task
        self.db_root_dir = db_root_dir
        self.max_rollout_steps = max_rollout_steps
        self.max_depth = max_depth
        self.exploration_constant = exploration_constant
        self.save_root_dir = save_root_dir
    
    def select(self, node: MCTSNode) -> MCTSNode:
        current = node
        while current.children and not current.is_terminal():
            if not all(child.N > 0 for child in current.children):
                return next(child for child in current.children if child.N == 0)
            
            current = max(current.children, key=lambda child: (child.Q / child.N) + self.exploration_constant * math.sqrt(math.log(current.N) / child.N))
        return current
    
    def expand(self, node: MCTSNode) -> List[MCTSNode]:
        assert node.children == [], f"Children nodes of node {node.node_type} before expansion is not empty"
        valid_action_space = get_valid_action_space_for_node(node)
        for action in valid_action_space:
            action_nodes = action.create_children_nodes(node, self.llm_kwargs)
            node.children.extend(action_nodes)
        
        random.shuffle(node.children)
        
        # three special actions: EndAction, SQLGenerationAction, SQLRevisionAction
        # they only generate one child node each time
        # n_special_actions = len([action for action in valid_action_space if isinstance(action, (EndAction, SQLGenerationAction, SQLRevisionAction))])
        # n_not_special_actions = len([action for action in valid_action_space if not isinstance(action, (EndAction, SQLGenerationAction, SQLRevisionAction))])
        # assert len(node.children) == \
        #     n_not_special_actions * self.llm_kwargs.get("n", 1) + \
        #     n_special_actions * 1, \
        #     f"Number of children nodes is not expected, expected: {n_not_special_actions * self.llm_kwargs.get('n', 1) + n_special_actions * 1}, actual: {len(node.children)}"

    def simulate(self, node: MCTSNode) -> MCTSNode:
        assert node.children == [], f"Node before simulation have non-empty children"
        current = node
        while not current.is_terminal():
            self.expand(current)
            current = random.choice(current.children)
        return current

    def backpropagate(self, node: MCTSNode):
        print("Backpropagate, Final SQL Query: ", node.final_sql_query)
        current = node
        if current.N == 0:
            reward = self.reward_model.get_reward(current)
        else:
            reward = current.Q / current.N
        while current is not None:
            current.N += 1
            current.Q += reward
            current = current.parent_node
    
    def find_all_end_nodes(self, node: MCTSNode) -> List[MCTSNode]:
        if node.node_type == MCTSNodeType.END:
            return [node]
        else:
            end_nodes = []
            for child in node.children:
                end_nodes.extend(self.find_all_end_nodes(child))
            return end_nodes
    
    def find_all_valid_reasoning_paths(self, node: MCTSNode) -> List[List[MCTSNode]]:
        end_nodes = self.find_all_end_nodes(node)
        reasoning_paths = []
        for end_node in end_nodes:
            reasoning_paths.append(end_node.path_nodes)
        return reasoning_paths
    
    def solve(self):
        schema_context= "\n".join([build_table_ddl_statement(
            self.task.table_schema_dict[table_name].to_dict(), 
            add_value_description=True, # new feature
            add_column_description=True,
            add_value_examples=True,
            add_expanded_column_name=True
        ) for table_name in self.task.table_schema_dict])
        root_node = MCTSNode(MCTSNodeType.ROOT,
                             parent_node=None,
                             parent_action=None,
                             depth=0,
                             db_id=self.task.db_id,
                             db_root_dir=self.db_root_dir,
                             original_question=self.task.question,
                             hint=self.task.evidence,
                            #  schema_context=self.task.schema_context,
                             schema_context=schema_context,
                             table_schema_dict=self.task.table_schema_dict)
        root_node.path_nodes = [root_node]
        
        for _ in range(self.max_rollout_steps):
            print(f"Question ID: {self.task.question_id}, Rollout step {_ + 1} / {self.max_rollout_steps}")
            leaf_node = self.select(root_node)
            if leaf_node.is_terminal():
                self.backpropagate(leaf_node)
                continue
            self.expand(leaf_node)
            leaf_node = random.choice(leaf_node.children)
            end_node = self.simulate(leaf_node)
            self.backpropagate(end_node)
        
        all_valid_reasoning_paths = self.find_all_valid_reasoning_paths(root_node)
        save_path = Path(self.save_root_dir) / f"{self.task.question_id}.pkl"
        print(f"Question ID: {self.task.question_id} done, Number of valid reasoning paths: {len(all_valid_reasoning_paths)}")
        with open(save_path, "wb") as f:
            pickle.dump(all_valid_reasoning_paths, f)

        
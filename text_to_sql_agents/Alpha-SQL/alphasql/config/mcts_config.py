from pydantic import BaseModel
from typing import Dict, Any, Optional

class MCTSConfig(BaseModel):
    """
    Configuration for the MCTS Runner.
    """
    tasks_file_path: str
    subset_file_path: Optional[str]
    db_root_dir: str
    n_processes: int
    max_rollout_steps: int
    max_depth: int
    exploration_constant: float
    save_root_dir: str
    mcts_model_kwargs: Dict[str, Any]
    reward_model_kwargs: Optional[Dict[str, Any]] = None
    random_seed: Optional[int] = 42
import inspect
from threading import Lock
from typing import Any, Dict, Tuple

class PipelineManager:
    _instance = None
    _lock = Lock()

    def __new__(cls, pipeline_setup: Dict[str, Any] = None):
        """
        Ensures a singleton instance of PipelineManager.

        Args:
            pipeline_setup (Dict[str, Any], optional): The setup dictionary for the pipeline. Required for initialization.

        Returns:
            PipelineManager: The singleton instance of the class.

        Raises:
            ValueError: If the pipeline_setup is not provided during the first initialization.
        """
        if pipeline_setup is not None:
            with cls._lock:
                cls._instance = super(PipelineManager, cls).__new__(cls)
                cls._instance.pipeline_setup = pipeline_setup
                cls._instance._init(pipeline_setup)
        elif cls._instance is None:
            raise ValueError("pipeline_setup dictionary must be provided for initialization")
        return cls._instance

    def _init(self, pipeline_setup: Dict[str, Any]):
        """
        Custom initialization logic using the pipeline_setup dictionary.

        Args:
            pipeline_setup (Dict[str, Any]): The setup dictionary for the pipeline.
        """
        self.generate_db_schema = pipeline_setup.get("generate_db_schema", {})
        self.extract_col_value = pipeline_setup.get("extract_col_value", {})
        self.extract_query_noun = pipeline_setup.get("extract_query_noun", {})
        self.column_retrieve_and_other_info = pipeline_setup.get("column_retrieve_and_other_info", {})
        self.candidate_generate = pipeline_setup.get("candidate_generate", {})
        self.align_correct = pipeline_setup.get("align_correct", {})
        self.vote = pipeline_setup.get("vote", {})
    
    def get_model_para(self, **kwargs: Any) -> dict:
        """
        Retrieves the prompt, engine, and parser for the current node based on the pipeline setup.

        Args:
            **kwargs: Additional keyword arguments for the prompt.

        Returns:
            Tuple[Any, Any, Any]: The prompt, engine, and parser instances.

        Raises:
            ValueError: If the engine is not specified for the node.
        """
        frame = inspect.currentframe()
        caller_frame = frame.f_back
        node_name = caller_frame.f_code.co_name
        
        node_setup = self.pipeline_setup.get(node_name, {})
                
        return node_setup,node_name
    

import os
import pickle
from threading import Lock
from pathlib import Path

from typing import Callable, Dict, List, Any
from runner.execution import compare_sqls


class DatabaseManager:
    """
    A singleton class to manage database operations including schema generation, 
    querying LSH and vector databases, and managing column profiles.
    """
    _instance = None
    _lock = Lock()

    def __new__(cls, db_mode=None,db_root_path=None,db_id=None):
        if (db_mode is not None) and (db_root_path is not None) and(db_id is not None):
            with cls._lock:
                if cls._instance is None:
                    cls._instance = super(DatabaseManager, cls).__new__(cls)
                    cls._instance._init(db_mode, db_root_path,db_id)
                elif cls._instance.db_id != db_id:
                    cls._instance._init(db_mode,db_root_path,db_id)
                return cls._instance
        else:
            if cls._instance is None:
                raise ValueError("DatabaseManager instance has not been initialized yet.")
            return cls._instance

    def _init(self, db_mode: str, db_root_path:str,db_id: str):
        """
        Initializes the DatabaseManager instance.

        Args:
            db_mode (str): The mode of the database (e.g., 'train', 'test').
            db_id (str): The database identifier.
        """
        self.db_mode = db_mode
        self.db_root_path=db_root_path
        self.db_id = db_id
        self._set_paths()

    def _set_paths(self):
        """Sets the paths for the database files and directories."""
        self.db_path = Path(self.db_root_path)/f"{self.db_mode}" / f"{self.db_mode}_databases" / self.db_id / f"{self.db_id}.sqlite"
        self.db_directory_path = Path(self.db_root_path)/f"{self.db_mode}" / f"{self.db_mode}_databases" / self.db_id
        self.db_json=Path(self.db_root_path)/"data_preprocess"/f"{self.db_mode}.json"
        self.db_tables=Path(self.db_root_path)/"data_preprocess"/"tables.json"
        self.db_fewshot_path=Path(self.db_root_path)/"fewshot"/"questions.json"
        self.db_fewshot2_path=Path(self.db_root_path)/"correct_fewshot2.json"
        self.emb_dir=Path(self.db_root_path)/"emb"

    @staticmethod
    def with_db_path(func: Callable):
        """
        Decorator to inject db_path as the first argument to the function.
        """
        def wrapper(self, *args, **kwargs):
            return func(self.db_path, *args, **kwargs)
        return wrapper

    @classmethod
    def add_methods_to_class(cls, funcs: List[Callable]):
        """
        Adds methods to the class with db_path automatically provided.

        Args:
            funcs (List[Callable]): List of functions to be added as methods.
        """
        for func in funcs:
            method = cls.with_db_path(func)
            setattr(cls, func.__name__, method)

# List of functions to be added to the class
functions_to_add = [
    compare_sqls
]

# Adding methods to the class
DatabaseManager.add_methods_to_class(functions_to_add)

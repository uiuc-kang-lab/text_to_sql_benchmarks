import json
import glob
import os
from uuid import UUID
from decimal import Decimal
from datetime import datetime, date, time, timedelta

from abc import ABC, abstractmethod

from func_timeout import FunctionTimedOut, func_timeout

from text2sql.data.sqlite_functions import (
    get_sqlite_database_file,
    query_sqlite_database,
    get_sqlite_schema,
)
from text2sql.data.schema_to_text import (
    get_m_schema_column_samples,
    get_mac_schema_column_samples,
    schema_to_basic_format,
    schema_to_datagrip_format,
    schema_to_mac_schema_format,
    schema_to_m_schema_format,
    schema_to_sql_create,
)


SCHEMA_FORMATS = [
    "basic",
    "basic_types",
    "basic_relations",
    "basic_types_relations",
    "datagrip",
    "sql_create",
    "m_schema",
    "mac_schema_basic",
    "mac_schema",
    "json_raw"
]


def list_supported_databases(dataset_base_path: str) -> list[str]:
    """find all sqlite databases in the dataset directory and return their names"""
    # handle nested or flat structure
    flat = [os.path.basename(p) for p in glob.glob(os.path.join(dataset_base_path, "*.sqlite"))]
    nested = [os.path.basename(p) for p in glob.glob(os.path.join(dataset_base_path, "**/*.sqlite"))]
    found_files = sorted(list(set(flat + nested)))
    database_names = [x.rsplit(".", 1)[0] for x in found_files]
    return database_names


class BaseDataset(ABC):
    supported_modes = SCHEMA_FORMATS

    @abstractmethod
    def get_databases(self) -> list[str]:
        pass

    @abstractmethod
    def get_database_schema(self, database_name: str) -> dict:
        pass

    @abstractmethod
    def query_database(self, database_name: str, query: str) -> list[dict]:
        pass

    def describe_database_schema(
        self,
        database_name: str,
        mode: str = "basic",
        table_descriptions: dict | None = None,
        max_examples: int | None = None,
    ) -> str:
        """return a string representation of the database schema"""
        if database_name not in self.databases:
            raise ValueError(f"Database '{database_name}' not in databases {self.databases}")
        if mode not in self.supported_modes:
            raise ValueError(f"Unknown schema mode '{mode}', supported modes are: {self.supported_modes}")
        schema = self.get_database_schema(database_name)
        if mode == "basic":
            return schema_to_basic_format(database_name, schema, include_types=False, include_relations=False)
        if mode == "basic_types":
            return schema_to_basic_format(database_name, schema, include_types=True, include_relations=False)
        if mode == "basic_relations":
            return schema_to_basic_format(database_name, schema, include_types=False, include_relations=True)
        if mode == "basic_types_relations":
            return schema_to_basic_format(database_name, schema, include_types=True, include_relations=True)
        elif mode == "sql_create":
            return schema_to_sql_create(database_name, schema)
        elif mode == "datagrip":
            return schema_to_datagrip_format(database_name, schema)
        elif mode == "m_schema":
            column_parameters = {"database_name": database_name, "schema": schema}
            if max_examples is not None:
                column_parameters["max_examples"] = max_examples
            column_samples = get_m_schema_column_samples(self, **column_parameters)
            return schema_to_m_schema_format(database_name, schema, column_samples)
        elif mode == "mac_schema_basic":
            if table_descriptions is not None:
                raise ValueError("table_descriptions should be None for mac_schema_basic mode")
            column_parameters = {"database_name": database_name, "schema": schema}
            if max_examples is not None:
                column_parameters["max_examples"] = max_examples
            column_samples = get_mac_schema_column_samples(self, **column_parameters)
            return schema_to_mac_schema_format(database_name, schema, column_samples)
        elif mode == "mac_schema":
            if table_descriptions is None:
                raise ValueError("table_descriptions dict is required for mac_schema mode")
            column_parameters = {"database_name": database_name, "schema": schema}
            if max_examples is not None:
                column_parameters["max_examples"] = max_examples
            column_samples = get_mac_schema_column_samples(self, **column_parameters)
            return schema_to_mac_schema_format(database_name, schema, column_samples, table_descriptions)
        elif mode =="json_raw":
            return json.dumps(schema, indent=4)


    def validate_query(self, database_name: str, query: str, timeout_secs: int = 30) -> dict:
        """validate the query against the database schema"""
        try:
            # Explicitly catch FunctionTimedOut
            result = func_timeout(timeout_secs, self.query_database, args=(database_name, query))
            success: bool = True
            message: str = "ok"
        except FunctionTimedOut as e:
            # Handle timeout specifically
            result = []
            success: bool = False
            message: str = f"query timed out after 300 seconds"
        except Exception as e:
            # Handle other exceptions
            result = []
            success: bool = False
            message: str = f"error - {type(e).__name__}: {str(e)}"
        return {"validated": success, "message": message, "execution_result": result}

    def normalize_db_query_results(self, data):
        # Matches the pydantic JSON serialization
        if isinstance(data, dict):
            return {key: self.normalize_db_query_results(value) for key, value in data.items()}
        elif isinstance(data, list):
            return [self.normalize_db_query_results(item) for item in data]
        elif isinstance(data, datetime):
            if data.microsecond:
                return data.strftime("%Y-%m-%dT%H:%M:%S.%f")
            return data.strftime("%Y-%m-%dT%H:%M:%S")
        elif isinstance(data, date):
            return data.strftime("%Y-%m-%d")
        elif isinstance(data, time):
            return data.strftime("%H:%M:%S")
        elif isinstance(data, timedelta):
            years = data.days // 365
            remaining_days = data.days % 365
            duration = f"P{years}Y"
            if remaining_days:
                duration += f"{remaining_days}D"
            return duration
        elif isinstance(data, (UUID, Decimal)):
            return str(data)
        elif isinstance(data, bytes):
            return data.hex()
        return data


class SqliteDataset(BaseDataset):
    def __init__(self, base_data_path: str):
        """initialize an sql dataset manager

        list, describe and query sqlite databases from sqlite based datasets.
        the base path should be the main directory of the databases,
        e.g. for BIRD, "<my_path_to>/bird/train/train_databases"

        Args:
            base_data_path (str): the base path of the dataset containing the databases
        """
        self.base_data_path = base_data_path
        self.databases = list_supported_databases(base_data_path)

    def get_databases(self) -> list[str]:
        """return a list of the names of the sqlite databases in the dataset"""
        return self.databases

    def get_schema_description_modes(self) -> list[str]:
        """return a list of the supported schema modes"""
        return self.supported_modes

    def get_database_path(self, database_name: str) -> str:
        """return the path to the sqlite database file"""
        if database_name not in self.databases:
            raise ValueError(f"Database '{database_name}' not found in '{self.base_data_path}'")
        return get_sqlite_database_file(self.base_data_path, database_name)

    def get_database_schema(self, database_name: str) -> dict:
        """return a dict of the database schema"""
        return get_sqlite_schema(self.base_data_path, database_name)

    def query_database(self, database_name: str, query: str) -> list[dict]:
        """return the results of the query as a list of dictionaries"""
        # connection = self.manager.get_connection(self.get_database_path(database_name))
        # return query_sqlite_database_from_connection(connection, query)
        return query_sqlite_database(self.base_data_path, database_name, query)

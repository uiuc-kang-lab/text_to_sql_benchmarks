from alphasql.llm_call.prompt_factory import get_prompt
from alphasql.llm_call.openai_llm import call_openai
from alphasql.database.sql_execution import (
    SQLExecutionResultType,
    cached_execute_sql_with_timeout,
    normalize_sql,
    is_valid_execution_result,
    format_execution_result
)
from alphasql.database.schema import TableSchema
from alphasql.database.utils import build_table_ddl_statement
from typing import Dict, Any, List, Optional, Tuple 
from enum import Enum
from pathlib import Path
from collections import defaultdict
import copy
import json
import re
import random

SQL_GENERATION_LLM_KWARGS_TEMPERATURE = 0.8
SQL_REVISION_LLM_KWARGS_TEMPERATURE = 0.8
SQL_GENERATION_LLM_KWARGS_N = 5
SQL_REVISION_LLM_KWARGS_N = 5

SQL_VALIDATION_MAX_TRIES = 15

class MCTSAction:
    def create_children_nodes(self, node: "MCTSNode", llm_kwargs: Dict[str, Any]) -> List["MCTSNode"]:
        raise NotImplementedError()

class RaphraseQuestionAction(MCTSAction):
    """
    Raphrase the question to be more specific.
    
    Valid previous nodes:
    - Root node
    """
    def create_children_nodes(self, node: "MCTSNode", llm_kwargs: Dict[str, Any]) -> List["MCTSNode"]:
        question = node.original_question
        hint = node.hint
        prompt = get_prompt(
            template_name="raphrase_question",
            template_args={"QUESTION": question, "HINT": hint}
        )
        responses = call_openai(prompt, **llm_kwargs)
        responses = list(set(responses))
        nodes = []
        for response in responses:
            child_node = copy.deepcopy(node)
            child_node.node_type = MCTSNodeType.REPHRASE_QUESTION
            child_node.parent_node = node
            child_node.parent_action = self
            child_node.depth = node.depth + 1
            child_node.children = []
            child_node.path_nodes = node.path_nodes + [child_node]
            child_node.rephrased_question = response
            nodes.append(child_node)
        return nodes

class SchemaSelectionAction(MCTSAction):
    """
    Select the schema context that is most relevant to the question.
    
    Valid previous nodes:
    - Root node
    - Raphrase question node
    - Identify column values node
    - Identify column functions node
    """
    def create_children_nodes(self, node: "MCTSNode", llm_kwargs: Dict[str, Any]) -> List["MCTSNode"]:
        question = node.rephrased_question if node.rephrased_question else node.original_question
        hint = node.hint
        schema_context = node.schema_context
        previous_thoughts = ""
        for path_node in node.path_nodes:
            if isinstance(path_node.parent_action, IdentifyColumnValuesAction):
                previous_thoughts += f"Identify column values: {path_node.identified_column_values}\n"
            elif isinstance(path_node.parent_action, IdentifyColumnFunctionsAction):
                previous_thoughts += f"Identify column functions: {path_node.identified_column_functions}\n"
        hint += f"\n\nHere are my previous thoughts:\n{previous_thoughts}" if previous_thoughts else ""
        prompt = get_prompt(
            template_name="schema_selection",
            template_args={"QUESTION": question, "HINT": hint, "SCHEMA_CONTEXT": schema_context}
        )
        nodes = []
        all_schema_selection_dicts = []
        while len(nodes) < llm_kwargs["n"]:
            new_llm_kwargs = copy.deepcopy(llm_kwargs)
            new_llm_kwargs["n"] = llm_kwargs["n"] - len(nodes)
            responses = call_openai(prompt, **new_llm_kwargs)
            for response in responses:
                child_node = copy.deepcopy(node)
                child_node.node_type = MCTSNodeType.SCHEMA_SELECTION
                child_node.parent_node = node
                child_node.parent_action = self
                child_node.depth = node.depth + 1
                child_node.children = []
                child_node.path_nodes = node.path_nodes + [child_node]
                new_table_schema_dict, schema_selection_dict = self.select_schema(child_node.table_schema_dict, response)
                if new_table_schema_dict:
                    child_node.selected_schema_dict = new_table_schema_dict
                    schema_context_ddl_list = [build_table_ddl_statement(
                        child_node.selected_schema_dict[table_name].to_dict(), 
                        add_value_description=True, # new feature
                        add_column_description=True,
                        add_value_examples=True,
                        add_expanded_column_name=True
                    ) for table_name in child_node.selected_schema_dict]
                    random.shuffle(schema_context_ddl_list) # new feature
                    child_node.selected_schema_context = "\n".join(schema_context_ddl_list)
                    nodes.append(child_node)
                    all_schema_selection_dicts.append(schema_selection_dict)
                else:
                    continue
        new_nodes = []
        hash_selection_dict_fn = lambda schema_selection_dict: frozenset([(table_name.lower(), column_name.lower()) for table_name, column_names in schema_selection_dict.items() for column_name in column_names])
        temp_set = set()
        for node, schema_selection_dict in zip(nodes, all_schema_selection_dicts):
            if hash_selection_dict_fn(schema_selection_dict) not in temp_set:
                temp_set.add(hash_selection_dict_fn(schema_selection_dict))
                new_nodes.append(node)
        return new_nodes[:llm_kwargs["n"]]
    
    def select_schema(self, table_schema_dict: Dict[str, TableSchema], schema_selection_response: str) -> Optional[Tuple[Dict[str, TableSchema], Dict[str, List[str]]]]:
        try:
            schema_selection_dict = json.loads(re.search(r"```json\n(.*)```", schema_selection_response, flags=re.DOTALL).group(1))
            # del schema_selection_dict["thinking"]
        except Exception as e:
            # print(schema_selection_response)
            print(f"Error parsing schema selection response: {e}")
            return None, None

        selected_table_names_lower = [selected_table_name.lower() for selected_table_name in schema_selection_dict.keys()]
        
        new_table_schema_dict = {}
        for selected_table_name, selected_column_names in schema_selection_dict.items():
            for original_table_name, original_table_schema in table_schema_dict.items():
                if selected_table_name.lower() == original_table_name.lower():
                    new_table_schema = TableSchema(table_name=original_table_name, columns={})
                    for original_column_name, original_column_schema in original_table_schema.columns.items():
                        is_selected = False
                        for selected_column_name in selected_column_names:
                            if selected_column_name.lower() == original_column_name.lower():
                                is_selected = True
                                break
                        if original_column_schema.primary_key:
                            # if the column is a primary key, it must be selected
                            is_selected = True
                        for target_table_name, target_column_name in original_column_schema.foreign_keys:
                            if target_table_name.lower() in selected_table_names_lower:
                                # if the column is a foreign key and the target table is selected, it must be selected
                                is_selected = True
                                break
                        for source_table_name, source_column_name in original_column_schema.referenced_by:
                            if source_table_name.lower() in selected_table_names_lower:
                                # if the column is a referenced by and the source table is selected, it must be selected
                                is_selected = True
                                break
                        if is_selected:
                            new_column_schema = copy.deepcopy(original_column_schema)
                            _foreign_keys = []
                            _referenced_by = []
                            for target_table_name, target_column_name in original_column_schema.foreign_keys:
                                if target_table_name.lower() in selected_table_names_lower:
                                    _foreign_keys.append((target_table_name, target_column_name))
                            for source_table_name, source_column_name in original_column_schema.referenced_by:
                                if source_table_name.lower() in selected_table_names_lower:
                                    _referenced_by.append((source_table_name, source_column_name))
                            new_column_schema.foreign_keys = _foreign_keys
                            new_column_schema.referenced_by = _referenced_by
                            new_table_schema.columns[original_column_name] = new_column_schema
                    new_table_schema_dict[original_table_name] = new_table_schema
        
        return new_table_schema_dict, schema_selection_dict

class IdentifyColumnValuesAction(MCTSAction):
    """
    Identify the column values that are most relevant to the question.
    
    Valid previous nodes:
    - Root node
    - Raphrase question node
    - Schema selection node
    - Identify column functions node
    """
    def create_children_nodes(self, node: "MCTSNode", llm_kwargs: Dict[str, Any]) -> List["MCTSNode"]:
        question = node.rephrased_question if node.rephrased_question else node.original_question
        hint = node.hint
        schema_context = node.selected_schema_context if node.selected_schema_context else node.schema_context
        previous_thoughts = ""
        for path_node in node.path_nodes:
            if isinstance(path_node.parent_action, IdentifyColumnFunctionsAction):
                previous_thoughts += f"Identify column functions: {path_node.identified_column_functions}\n"
        hint += f"\n\nHere are my previous thoughts:\n{previous_thoughts}" if previous_thoughts else ""
        prompt = get_prompt(
            template_name="identify_column_values",
            template_args={"QUESTION": question, "HINT": hint, "SCHEMA_CONTEXT": schema_context}
        )
        responses = call_openai(prompt, **llm_kwargs)
        responses = list(set(responses))
        nodes = []
        for response in responses:
            child_node = copy.deepcopy(node)
            child_node.node_type = MCTSNodeType.IDENTIFY_COLUMN_VALUES
            child_node.parent_node = node
            child_node.parent_action = self
            child_node.depth = node.depth + 1
            child_node.children = []
            child_node.path_nodes = node.path_nodes + [child_node]
            child_node.identified_column_values = response
            nodes.append(child_node)
        return nodes

class IdentifyColumnFunctionsAction(MCTSAction):
    """
    Identify the column functions that are most relevant to the question.
    
    Valid previous nodes:
    - Root node
    - Raphrase question node
    - Schema selection node
    - Identify column values node
    """
    
    def create_children_nodes(self, node: "MCTSNode", llm_kwargs: Dict[str, Any]) -> List["MCTSNode"]:
        question = node.rephrased_question if node.rephrased_question else node.original_question
        hint = node.hint
        schema_context = node.selected_schema_context if node.selected_schema_context else node.schema_context
        previous_thoughts = ""
        for path_node in node.path_nodes:
            if isinstance(path_node.parent_action, IdentifyColumnValuesAction):
                previous_thoughts += f"Identify column values: {path_node.identified_column_values}\n"
        hint += f"\n\nHere are my previous thoughts:\n{previous_thoughts}" if previous_thoughts else ""
        prompt = get_prompt(
            template_name="identify_column_functions",
            template_args={"QUESTION": question, "HINT": hint, "SCHEMA_CONTEXT": schema_context}
        )
        responses = call_openai(prompt, **llm_kwargs)
        responses = list(set(responses))
        nodes = []
        for response in responses:
            child_node = copy.deepcopy(node)
            child_node.node_type = MCTSNodeType.IDENTIFY_COLUMN_FUNCTIONS
            child_node.parent_node = node
            child_node.parent_action = self
            child_node.depth = node.depth + 1
            child_node.children = []
            child_node.path_nodes = node.path_nodes + [child_node]
            child_node.identified_column_functions = response
            nodes.append(child_node)
        return nodes

class SQLGenerationAction(MCTSAction):
    """
    Generate the SQL query.
    
    Valid previous nodes:
    - Root node
    - Raphrase question node
    - Schema selection node
    - Identify column values node
    - Identify column functions node
    """
    def create_children_nodes_without_self_consistency(self, node: "MCTSNode", llm_kwargs: Dict[str, Any]) -> List["MCTSNode"]:
        question = node.rephrased_question if node.rephrased_question else node.original_question
        hint = node.hint
        schema_context = node.selected_schema_context if node.selected_schema_context else node.schema_context
        previous_thoughts = ""
        for path_node in node.path_nodes:
            if isinstance(path_node.parent_action, IdentifyColumnValuesAction):
                previous_thoughts += f"Identify column values: {path_node.identified_column_values}\n"
            elif isinstance(path_node.parent_action, IdentifyColumnFunctionsAction):
                previous_thoughts += f"Identify column functions: {path_node.identified_column_functions}\n"
        hint += f"\n\nHere are my previous thoughts:\n{previous_thoughts}" if previous_thoughts else ""
        prompt = get_prompt(
            template_name="sql_generation",
            template_args={"QUESTION": question, "HINT": hint, "SCHEMA_CONTEXT": schema_context}
        )
        nodes = []
        valid_sql_query_tries = 0
        while len(nodes) < llm_kwargs["n"]:
            new_llm_kwargs = copy.deepcopy(llm_kwargs)
            new_llm_kwargs["n"] = llm_kwargs["n"] - len(nodes)
            responses = call_openai(prompt, **new_llm_kwargs)
            for response in responses:
                child_node = copy.deepcopy(node)
                child_node.node_type = MCTSNodeType.SQL_GENERATION
                child_node.parent_node = node
                child_node.parent_action = self
                child_node.depth = node.depth + 1
                child_node.children = []
                child_node.path_nodes = node.path_nodes + [child_node]
                sql_query = self.extract_sql_query_answer(response)
                
                if sql_query:
                    db_path = Path(node.db_root_dir) / node.db_id / f"{node.db_id}.sqlite"
                    sql_query_execution_result = cached_execute_sql_with_timeout(db_path, sql_query)
                    if is_valid_execution_result(sql_query_execution_result) or valid_sql_query_tries >= SQL_VALIDATION_MAX_TRIES:
                        child_node.sql_query = sql_query
                        nodes.append(child_node)
                    else:
                        valid_sql_query_tries += 1
        return nodes
    
    def create_children_nodes(self, node: "MCTSNode", llm_kwargs: Dict[str, Any]) -> List["MCTSNode"]:
        question = node.rephrased_question if node.rephrased_question else node.original_question
        hint = node.hint
        schema_context = node.selected_schema_context if node.selected_schema_context else node.schema_context
        previous_thoughts = ""
        for path_node in node.path_nodes:
            if isinstance(path_node.parent_action, IdentifyColumnValuesAction):
                previous_thoughts += f"Identify column values: {path_node.identified_column_values}\n"
            elif isinstance(path_node.parent_action, IdentifyColumnFunctionsAction):
                previous_thoughts += f"Identify column functions: {path_node.identified_column_functions}\n"
        hint += f"\n\nHere are my previous thoughts:\n{previous_thoughts}" if previous_thoughts else ""
        prompt = get_prompt(
            template_name="sql_generation",
            template_args={"QUESTION": question, "HINT": hint, "SCHEMA_CONTEXT": schema_context}
        )
        
        child_node = copy.deepcopy(node)
        child_node.node_type = MCTSNodeType.SQL_GENERATION
        child_node.parent_node = node
        child_node.parent_action = self
        child_node.depth = node.depth + 1
        child_node.children = []
        child_node.path_nodes = node.path_nodes + [child_node]
        sql_query = None
        db_path = Path(node.db_root_dir) / node.db_id / f"{node.db_id}.sqlite"
        while not sql_query:
            sql_query, consistency_score, is_valid_sql_query = self.generate_most_consistent_sql_query(prompt, llm_kwargs, db_path)
        child_node.sql_query = sql_query
        child_node.consistency_score = consistency_score
        child_node.is_valid_sql_query = is_valid_sql_query
        return [child_node]

    def generate_most_consistent_sql_query(self, prompt: str, llm_kwargs: Dict[str, Any], db_path: str) -> Optional[str]:
        # new_llm_kwargs = copy.deepcopy(llm_kwargs)
        # new_llm_kwargs["temperature"] = SQL_GENERATION_LLM_KWARGS_TEMPERATURE
        # new_llm_kwargs["n"] = SQL_GENERATION_LLM_KWARGS_N
        all_sql_queries = []
        result_groups = defaultdict(list)
        valid_sql_query_tries = 0
        while len(all_sql_queries) < SQL_GENERATION_LLM_KWARGS_N:
            # prevent infinite loop
            if valid_sql_query_tries >= SQL_VALIDATION_MAX_TRIES and len(all_sql_queries) > 0:
                break
            new_llm_kwargs = copy.deepcopy(llm_kwargs)
            new_llm_kwargs["n"] = SQL_GENERATION_LLM_KWARGS_N - len(all_sql_queries)
            new_llm_kwargs["temperature"] = SQL_GENERATION_LLM_KWARGS_TEMPERATURE
            responses = call_openai(prompt, **new_llm_kwargs)
            for response in responses:
                sql_query = self.extract_sql_query_answer(response)
                if sql_query is None:
                    continue
                sql_query_execution_result = cached_execute_sql_with_timeout(db_path, sql_query)
                if is_valid_execution_result(sql_query_execution_result) or valid_sql_query_tries >= SQL_VALIDATION_MAX_TRIES:
                    all_sql_queries.append(sql_query)
                    if is_valid_execution_result(sql_query_execution_result):
                        result_groups[frozenset(sql_query_execution_result.result)].append(sql_query)
                else:
                    valid_sql_query_tries += 1
        
        if len(result_groups) == 0 and len(all_sql_queries) > 0:
            return random.choice(all_sql_queries), 0, False
        else:
            most_consistent_sql_query = None
            max_group_size = 0
            all_sql_queries_size = 0
            for result, sql_queries in result_groups.items():
                all_sql_queries_size += len(sql_queries)
                if len(sql_queries) > max_group_size:
                    most_consistent_sql_query = random.choice(sql_queries)
                    max_group_size = len(sql_queries)
            return most_consistent_sql_query, max_group_size / all_sql_queries_size, True

    # def extract_sql_query_answer(self, sql_generation_response: str) -> str:
    #     try:
    #         return normalize_sql(re.search(r"<FINAL_ANSWER>(.*)</FINAL_ANSWER>", sql_generation_response, flags=re.DOTALL).group(1).strip())
    #     except Exception as e:
    #         return None
    
    def extract_sql_query_answer(self, sql_generation_response: str) -> str:
        try:
            sql_query = re.search(r"<sql>(.*)</sql>", sql_generation_response, flags=re.DOTALL).group(1).strip()
            return normalize_sql(sql_query)
        except Exception as e:
            print(f"Error parsing sql generation response: {e}")
            return None

class SQLRevisionAction(MCTSAction):
    """
    Revise the SQL query with the given context.
    
    Valid previous nodes:
    - Identify column values node
    - Identify column functions node
    - SQL generation node
    """
    def create_children_nodes_without_self_consistency(self, node: "MCTSNode", llm_kwargs: Dict[str, Any]) -> List["MCTSNode"]:
        question = node.rephrased_question if node.rephrased_question else node.original_question
        hint = node.hint
        schema_context = node.selected_schema_context if node.selected_schema_context else node.schema_context
        previous_thoughts = ""
        for path_node in node.path_nodes:
            if isinstance(path_node.parent_action, IdentifyColumnValuesAction):
                previous_thoughts += f"Identify column values: {path_node.identified_column_values}\n"
            elif isinstance(path_node.parent_action, IdentifyColumnFunctionsAction):
                previous_thoughts += f"Identify column functions: {path_node.identified_column_functions}\n"
            elif isinstance(path_node.parent_action, SQLGenerationAction):
                sql_execution_result = cached_execute_sql_with_timeout(
                    Path(path_node.db_root_dir) / path_node.db_id / f"{path_node.db_id}.sqlite",
                    path_node.sql_query
                )
                sql_execution_result_str = format_execution_result(sql_execution_result)
                previous_thoughts += f"SQL generation: {path_node.sql_query}\nSQL execution result:\n{sql_execution_result_str}\n"
        hint += f"\n\nHere are my previous thoughts:\n{previous_thoughts}" if previous_thoughts else ""
        prompt = get_prompt(
            template_name="sql_revision",
            template_args={"QUESTION": question, "HINT": hint, "SCHEMA_CONTEXT": schema_context}
        )
        nodes = []
        valid_sql_query_tries = 0
        while len(nodes) < llm_kwargs["n"]:
            new_llm_kwargs = copy.deepcopy(llm_kwargs)
            new_llm_kwargs["n"] = llm_kwargs["n"] - len(nodes)
            responses = call_openai(prompt, **new_llm_kwargs)
            for response in responses:
                child_node = copy.deepcopy(node)
                child_node.node_type = MCTSNodeType.SQL_REVISION
                child_node.parent_node = node
                child_node.parent_action = self
                child_node.depth = node.depth + 1
                child_node.children = []
                child_node.path_nodes = node.path_nodes + [child_node]
                revised_sql_query = self.extract_sql_query_answer(response)
                if revised_sql_query:
                    db_path = Path(node.db_root_dir) / node.db_id / f"{node.db_id}.sqlite"
                    sql_query_execution_result = cached_execute_sql_with_timeout(db_path, revised_sql_query)
                    if is_valid_execution_result(sql_query_execution_result) or valid_sql_query_tries >= SQL_VALIDATION_MAX_TRIES:
                        child_node.revised_sql_query = revised_sql_query
                        nodes.append(child_node)
                    else:
                        valid_sql_query_tries += 1
        return nodes
    
    def create_children_nodes(self, node: "MCTSNode", llm_kwargs: Dict[str, Any]) -> List["MCTSNode"]:
        question = node.rephrased_question if node.rephrased_question else node.original_question
        hint = node.hint
        schema_context = node.selected_schema_context if node.selected_schema_context else node.schema_context
        previous_thoughts = ""
        for path_node in node.path_nodes:
            if isinstance(path_node.parent_action, IdentifyColumnValuesAction):
                previous_thoughts += f"Identify column values: {path_node.identified_column_values}\n"
            elif isinstance(path_node.parent_action, IdentifyColumnFunctionsAction):
                previous_thoughts += f"Identify column functions: {path_node.identified_column_functions}\n"
            elif isinstance(path_node.parent_action, SQLGenerationAction):
                sql_execution_result = cached_execute_sql_with_timeout(
                    Path(path_node.db_root_dir) / path_node.db_id / f"{path_node.db_id}.sqlite",
                    path_node.sql_query
                )
                sql_execution_result_str = format_execution_result(sql_execution_result)
                previous_thoughts += f"SQL generation: {path_node.sql_query}\nSQL execution result:\n{sql_execution_result_str}\n"
        hint += f"\n\nHere are my previous thoughts:\n{previous_thoughts}" if previous_thoughts else ""
        prompt = get_prompt(
            template_name="sql_revision",
            template_args={"QUESTION": question, "HINT": hint, "SCHEMA_CONTEXT": schema_context}
        )
        
        child_node = copy.deepcopy(node)
        child_node.node_type = MCTSNodeType.SQL_REVISION
        child_node.parent_node = node
        child_node.parent_action = self
        child_node.depth = node.depth + 1
        child_node.children = []
        child_node.path_nodes = node.path_nodes + [child_node]
        sql_query = None
        db_path = Path(node.db_root_dir) / node.db_id / f"{node.db_id}.sqlite"
        while not sql_query:
            sql_query, consistency_score, is_valid_sql_query = self.generate_most_consistent_sql_query(prompt, llm_kwargs, db_path)
        child_node.revised_sql_query = sql_query
        child_node.consistency_score = consistency_score
        child_node.is_valid_sql_query = is_valid_sql_query
        return [child_node]
    
    def generate_most_consistent_sql_query(self, prompt: str, llm_kwargs: Dict[str, Any], db_path: str) -> Optional[str]:
        # new_llm_kwargs = copy.deepcopy(llm_kwargs)
        # new_llm_kwargs["temperature"] = SQL_REVISION_LLM_KWARGS_TEMPERATURE
        # new_llm_kwargs["n"] = SQL_REVISION_LLM_KWARGS_N
        all_sql_queries = []
        result_groups = defaultdict(list)
        valid_sql_query_tries = 0
        while len(all_sql_queries) < SQL_REVISION_LLM_KWARGS_N:
            # prevent infinite loop
            if valid_sql_query_tries >= SQL_VALIDATION_MAX_TRIES and len(all_sql_queries) > 0:
                break
            new_llm_kwargs = copy.deepcopy(llm_kwargs)
            new_llm_kwargs["n"] = SQL_REVISION_LLM_KWARGS_N - len(all_sql_queries)
            new_llm_kwargs["temperature"] = SQL_REVISION_LLM_KWARGS_TEMPERATURE
            responses = call_openai(prompt, **new_llm_kwargs)
            for response in responses:
                sql_query = self.extract_sql_query_answer(response)
                if sql_query is None:
                    continue
                sql_query_execution_result = cached_execute_sql_with_timeout(db_path, sql_query)
                if is_valid_execution_result(sql_query_execution_result) or valid_sql_query_tries >= SQL_VALIDATION_MAX_TRIES:
                    all_sql_queries.append(sql_query)
                    if is_valid_execution_result(sql_query_execution_result):
                        result_groups[frozenset(sql_query_execution_result.result)].append(sql_query)
                else:
                    valid_sql_query_tries += 1
        
        if len(result_groups) == 0 and len(all_sql_queries) > 0:
            return random.choice(all_sql_queries), 0, False
        else:
            most_consistent_sql_query = None
            max_group_size = 0
            all_sql_queries_size = 0
            for result, sql_queries in result_groups.items():
                all_sql_queries_size += len(sql_queries)
                if len(sql_queries) > max_group_size:
                    most_consistent_sql_query = random.choice(sql_queries)
                    max_group_size = len(sql_queries)
            return most_consistent_sql_query, max_group_size / all_sql_queries_size, True
    
    # def extract_sql_query_answer(self, sql_revision_response: str) -> str:
    #     try:
    #         return normalize_sql(re.search(r"<FINAL_ANSWER>(.*)</FINAL_ANSWER>", sql_revision_response, flags=re.DOTALL).group(1).strip())
    #     except Exception:
    #         return None

    def extract_sql_query_answer(self, sql_revision_response: str) -> str:
        try:
            sql_query = re.search(r"<sql>(.*)</sql>", sql_revision_response, flags=re.DOTALL).group(1).strip()
            return normalize_sql(sql_query)
        except Exception as e:
            print(f"Error parsing sql revision response: {e}")
            return None

class EndAction(MCTSAction):
    """
    End the search.
    """
    def create_children_nodes(self, node: "MCTSNode", llm_kwargs: Dict[str, Any]) -> List["MCTSNode"]:
        assert node.node_type == MCTSNodeType.SQL_REVISION or node.node_type == MCTSNodeType.SQL_GENERATION
        child_node = copy.deepcopy(node)
        child_node.node_type = MCTSNodeType.END
        child_node.parent_node = node
        child_node.parent_action = self
        child_node.depth = node.depth + 1
        child_node.children = []
        child_node.path_nodes = node.path_nodes + [child_node]
        child_node.final_sql_query = node.sql_query if node.node_type == MCTSNodeType.SQL_GENERATION else node.revised_sql_query
        return [child_node]

class MCTSNodeType(Enum):
    ROOT = "root"
    REPHRASE_QUESTION = "rephrase_question"
    SCHEMA_SELECTION = "schema_selection"
    IDENTIFY_COLUMN_VALUES = "identify_column_values"
    IDENTIFY_COLUMN_FUNCTIONS = "identify_column_functions"
    SQL_REVISION = "sql_revision"
    SQL_GENERATION = "sql_generation"
    END = "end"

NODE_TYPE_TO_VALID_ACTIONS = {
    MCTSNodeType.ROOT: [
        RaphraseQuestionAction,
        IdentifyColumnValuesAction,
        IdentifyColumnFunctionsAction,
        SchemaSelectionAction,
        SQLGenerationAction
    ],
    MCTSNodeType.REPHRASE_QUESTION: [
        IdentifyColumnValuesAction,
        IdentifyColumnFunctionsAction,
        SchemaSelectionAction,
        SQLGenerationAction
    ],
    MCTSNodeType.SCHEMA_SELECTION: [
        IdentifyColumnValuesAction,
        IdentifyColumnFunctionsAction,
        SQLGenerationAction
    ],
    MCTSNodeType.IDENTIFY_COLUMN_VALUES: [
        IdentifyColumnFunctionsAction,
        SchemaSelectionAction,
        SQLGenerationAction
    ],
    MCTSNodeType.IDENTIFY_COLUMN_FUNCTIONS: [
        SchemaSelectionAction,
        IdentifyColumnValuesAction,
        SQLGenerationAction
    ],
    MCTSNodeType.SQL_GENERATION: [
        EndAction,
        SQLRevisionAction
    ],
    MCTSNodeType.SQL_REVISION: [
        EndAction
    ],
    MCTSNodeType.END: []
}

from typing import Dict, TypedDict, Callable
from langgraph.graph import END, StateGraph

from pipeline.generate_db_schema import generate_db_schema
from pipeline.extract_col_value import extract_col_value
from pipeline.extract_query_noun import extract_query_noun
from pipeline.column_retrieve_and_other_info import column_retrieve_and_other_info
from pipeline.candidate_generate import candidate_generate
from pipeline.align_correct import align_correct
from pipeline.vote import vote
from pipeline.evaluation import evaluation
import logging

### Graph State ###
class GraphState(TypedDict):
    """
    Represents the state of our graph.

    Attributes:
        keys: A dictionary where each key is a string.
    """
    keys: Dict[str, any]

class WorkflowBuilder:
    def __init__(self):
        self.workflow = StateGraph(GraphState)
        logging.info("Initialized WorkflowBuilder")

    def build(self, pipeline_nodes: str) -> None:
        """
        Builds the workflow based on the provided pipeline nodes.

        Args:
            pipeline_nodes (str): A string of pipeline node names separated by '+'.
        """
        nodes = pipeline_nodes.split("+")
        logging.info(f"Building workflow with nodes: {nodes}")
        self._add_nodes(nodes)
        self.workflow.set_entry_point(nodes[0])
        self._add_edges([(nodes[i], nodes[i+1]) for i in range(len(nodes) - 1)])
        self._add_edges([(nodes[-1], END)])
        logging.info("Workflow built successfully")

    def _add_nodes(self, nodes: list) -> None:
        """
        Adds nodes to the workflow.

        Args:
            nodes (list): A list of node names.
        """
        for node_name in nodes:
            if node_name in globals() and callable(globals()[node_name]):
                self.workflow.add_node(node_name, globals()[node_name])
                logging.info(f"Added node: {node_name}")
            else:
                logging.error(f"Node function '{node_name}' not found in global scope")

    def _add_edges(self, edges: list) -> None:
        """
        Adds edges between nodes in the workflow.

        Args:
            edges (list): A list of tuples representing the edges.
        """
        for src, dst in edges:
            self.workflow.add_edge(src, dst)
            logging.info(f"Added edge from {src} to {dst}")
    



def build_pipeline(pipeline_nodes: str) -> Callable:
    """
    Builds and compiles the pipeline based on the provided nodes.

    Args:
        pipeline_nodes (str): A string of pipeline node names separated by '+'.

    Returns:
        Callable: The compiled workflow application.
    """
    builder = WorkflowBuilder()
    builder.build(pipeline_nodes)
    app = builder.workflow.compile()
    logging.info("Pipeline built and compiled successfully")
    return app

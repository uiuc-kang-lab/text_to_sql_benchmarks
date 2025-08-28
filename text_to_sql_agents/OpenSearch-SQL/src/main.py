import argparse
import json
from datetime import datetime
from typing import Any, Dict, List
import argparse
from runner.run_manager import RunManager
import os

def load_dataset(data_path: str) -> List[Dict[str, Any]]:
    """
    Loads the dataset from the specified path.

    Args:
        data_path (str): Path to the data file.

    Returns:
        List[Dict[str, Any]]: The loaded dataset.
    """
    with open(data_path, 'r') as file:
        dataset = json.load(file)
    return dataset

def main(args):
    """
    Main function to run the pipeline with the specified configuration.
    """
##
    db_json=os.path.join(args.db_root_path,'data_preprocess',f'{args.data_mode}.json')
    

    dataset = load_dataset(db_json)

    run_manager = RunManager(args)
    run_manager.initialize_tasks(args.start,args.end,dataset)
    run_manager.run_tasks()
    run_manager.generate_sql_files()

if __name__ == '__main__':
    args_parser = argparse.ArgumentParser()
    args_parser.add_argument('--data_mode', type=str, required=True, help="Mode of the data to be processed.")
    args_parser.add_argument('--db_root_path', type=str, required=True, help="Path to the data file.")
    args_parser.add_argument('--pipeline_nodes', type=str, required=True, help="Pipeline nodes configuration.")
    args_parser.add_argument('--pipeline_setup', type=str, required=True, help="Pipeline setup in JSON format.")
    args_parser.add_argument('--use_checkpoint', action='store_true', help="Flag to use checkpointing.")
    args_parser.add_argument('--checkpoint_nodes', type=str, required=False, help="Checkpoint nodes configuration.")
    args_parser.add_argument('--checkpoint_dir', type=str, required=False, help="Directory for checkpoints.")
    args_parser.add_argument('--log_level', type=str, default='warning', help="Logging level.")
    args_parser.add_argument('--start', type=int, default=0, help="Start point")
    args_parser.add_argument('--end', type=int, default=1, help="End point")
    args = args_parser.parse_args()
    args.run_start_time = datetime.now().strftime("%Y-%m-%d-%H-%M-%S")

    if args.use_checkpoint:
        print('Using checkpoint')
        if not args.checkpoint_nodes:
            raise ValueError('Please provide the checkpoint nodes to use checkpoint')
        if not args.checkpoint_dir:
            raise ValueError('Please provide the checkpoint path to use checkpoint')
    
    main(args)

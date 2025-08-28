from alphasql.config.selection_config import SelectionConfig    
from alphasql.algorithm.selection.ensembled_selection import EnsembledSelection
from alphasql.algorithm.selection.two_stage_selection import TwoStageSelection
from pathlib import Path
import yaml
from typing import Union

class SelectionRunner:
    def __init__(self, config: Union[SelectionConfig, str]):
        if isinstance(config, str):
            config_path = Path(config)
            assert config_path.exists(), f"Config file {config_path} does not exist"
            if config_path.suffix == ".json":
                self.config = SelectionConfig.model_validate_json(config_path.read_text())
            elif config_path.suffix == ".yaml":
                self.config = SelectionConfig.model_validate(yaml.safe_load(config_path.read_text()))
            else:
                raise ValueError(f"Unsupported config file extension: {config_path.suffix}")
        else:
            self.config = config
        
        if not Path(self.config.results_dir).exists():
            raise ValueError(f"Results directory {self.config.results_dir} does not exist")
        
        if not Path(self.config.output_dir).exists():
            Path(self.config.output_dir).mkdir(parents=True, exist_ok=True)
    
    def run(self):
        EnsembledSelection.select_sql_query(self.config)
        # TwoStageSelection.select_sql_query(self.config)
        print("Selection finished")
        
if __name__ == "__main__":
    import sys
    if len(sys.argv) < 2:
        print("Usage: python -m alphasql.runner.selection_runner <config_path>")
        sys.exit(1)
    config_path = sys.argv[1]
    runner = SelectionRunner(config=config_path)
    runner.run()
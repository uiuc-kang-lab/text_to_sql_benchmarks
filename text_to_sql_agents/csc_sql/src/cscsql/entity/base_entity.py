from dataclasses import dataclass, field


@dataclass
class EvalArguments:
    run_time: str = field(default="20250525_000000", metadata={"help": "run_time"})
    source: str = field(default="bird", metadata={"help": "Dataset name."})
    gold_file: str = field(default="bird", metadata={"help": "gold_file"})
    gold_result_dir: str = field(default="bird", metadata={"help": "gold_result_dir"})
    pred_file: str = field(default="bird", metadata={"help": "pred_file"})
    db_path: str = field(default="bird", metadata={"help": "db_path"})
    ts_db_path: str = field(default="bird", metadata={"help": "ts_db_path"})
    mode: str = field(default="major_voting", metadata={"help": "eval mode"})
    eval_standard: str = field(default="major_voting", metadata={"help": "eval_standard"})
    save_pred_sqls: bool = field(default=True, metadata={"help": "save_pred_sql"})
    num_cpus: int = field(default=30, metadata={"help": "num_cpus"})
    timeout: float = field(default=30, metadata={"help": "timeout"})
    ckpt_id: str = field(default="", metadata={"help": "ckpt_id"})
    eval_name: str = field(default="", metadata={"help": "eval_name"})
    show_prefix: str = field(default="", metadata={"help": "show_prefix"})
    prompt_name: str = field(default="", metadata={"help": "prompt_name"})
    selection_vote: str = field(default="none", metadata={"help": "selection_vote"})
    prompt_mode: str = field(default="merge", metadata={"help": "prompt_mode"})
    n: int = field(default=8, metadata={"help": "n"})

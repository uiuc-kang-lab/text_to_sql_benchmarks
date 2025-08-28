# Copyright 2025 The HuggingFace Team. All rights reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
import dataclasses
import json
import logging
import os
import sys
from dataclasses import dataclass, field
from typing import Dict, Optional, Callable

import datasets
import torch
import transformers
from datasets import load_dataset
from transformers import set_seed
from transformers.trainer import TRAINER_STATE_NAME
from transformers.trainer_callback import ExportableState
from transformers.trainer_utils import get_last_checkpoint, PREFIX_CHECKPOINT_DIR

from cscsql.service.grpo.configs import GRPOConfig
from cscsql.service.grpo.nl2sql_reward import (format_reward,
                                               execute_accuracy_reward,
                                               selection_vote_reward,
                                               link_table_reward,
                                               link_column_reward,
                                               get_predict_columns_from_schema,
                                               link_column_from_sql_reward)
# from open_r1.rewards import (
#     accuracy_reward,
#     code_reward,
#     format_reward,
#     get_code_format_reward,
#     get_cosine_scaled_reward,
#     get_repetition_penalty_reward,
#     len_reward,
#     reasoning_steps_reward,
#     tag_count_reward,
# )

from cscsql.service.grpo.model_utils import get_model, get_tokenizer
from cscsql.service.grpo.callbacks import get_callbacks
from cscsql.service.grpo.wandb_logging import init_wandb_training
from trl import GRPOTrainer
from trl import (ModelConfig, ScriptArguments, TrlParser, get_peft_config)

logger = logging.getLogger(__name__)


@dataclass
class GRPOScriptArguments(ScriptArguments):
    """
    Script arguments for the GRPO training script.

    Args:
        reward_funcs (`list[str]`):
            List of reward functions. Possible values: 'accuracy', 'format', 'reasoning_steps', 'cosine', 'repetition_penalty', 'length', 'tag_count', 'code', 'code_format'.
        cosine_min_value_wrong (`float`):
            Minimum reward for cosine scaling for wrong answers.
        cosine_max_value_wrong (`float`):
            Maximum reward for cosine scaling for wrong answers.
        cosine_min_value_correct (`float`):
            Minimum reward for cosine scaling for correct answers.
        cosine_max_value_correct (`float`):
            Maximum reward for cosine scaling for correct answers.
        cosine_max_len (`int`):
            Maximum length for cosine scaling.
        code_language (`str`):
            Language for code format reward.
    """
    dataset_path: str = field(
        default=None,
        metadata={"help": "Dataset path."}
    )

    reward_funcs: list[str] = field(
        default_factory=lambda: ["accuracy", "format", "tag_count"],
        metadata={
            "help": "List of reward functions. Possible values: 'accuracy', 'format', 'reasoning_steps', 'cosine', 'repetition_penalty', 'length', tag_count', 'code', 'code_format'"
        },
    )
    cosine_min_value_wrong: float = field(
        default=0.0,
        metadata={"help": "Minimum reward for wrong answers"},
    )
    cosine_max_value_wrong: float = field(
        default=-0.5,
        metadata={"help": "Maximum reward for wrong answers"},
    )
    cosine_min_value_correct: float = field(
        default=0.5,
        metadata={"help": "Minimum reward for correct answers"},
    )
    cosine_max_value_correct: float = field(
        default=1.0,
        metadata={"help": "Maximum reward for correct answers"},
    )
    cosine_max_len: int = field(
        default=1000,
        metadata={"help": "Maximum length for scaling"},
    )
    repetition_n_grams: int = field(
        default=3,
        metadata={"help": "Number of n-grams for repetition penalty reward"},
    )
    repetition_max_penalty: float = field(
        default=-1.0,
        metadata={"help": "Maximum (negative) penalty for for repetition penalty reward"},
    )
    code_language: str = field(
        default="python",
        metadata={
            "help": "Language for code format reward. Based on E2B supported languages https://e2b.dev/docs/code-interpreting/supported-languages",
            "choices": ["python", "javascript", "r", "java", "bash"],
        },
    )
    template_name: str = field(
        default="think",
        metadata={
            "help": "template_name",
            "choices": ["think", "ddl"],
        },
    )
    max_train_prompt_len: Optional[int] = field(
        default=7000,
        metadata={
            "help": "If set, the `max_model_len` to use for vLLM. This can be useful when running with reduced "
                    "`vllm_gpu_memory_utilization`, leading to a reduced KV cache size. If not set, vLLM will use the model "
                    "context size, which might be much larger than the KV cache, leading to inefficiencies."
        },
    )


def make_prefix1(dp: Dict, template_type='default'):
    question_raw = dp['instruction'] + dp.get("input", "")
    task_msg = "Please output only the final SQL query, starts with keyword `SELECT`."
    question_raw = question_raw.replace(task_msg, '')

    if template_type == 'default':
        """This works for any base model"""
        prefix = f"""{question_raw}\

Show your reason in <think> </think> tags. And return the final SQLite SQL query that starts with keyword `SELECT` in <answer> </answer> tags, \
for example <answer>SELECT AVG(rating_score) FROM movies</answer>. \
Let me solve this step by step."""
    return prefix


def make_prefix(dp: Dict, template_type='think',
                instruction_key='instruction'):
    other_input = dp.get("input", "")
    if "input_seq" in dp and instruction_key not in dp:
        question_raw = dp["input_seq"]
        if other_input:
            question_raw += other_input

        if template_type == "merge2":
            src_msg1 = "Make sure you only output the information that is asked in the question. If the question asks for a specific column, make sure to only include that column in the SELECT clause, nothing more."
            new_msg1 = "You should first carefully analyze each draft SQL, compare their differences, and then conduct further analysis based on user questions to determine which draft SQL is correct in the end."
            question_raw = question_raw.replace(src_msg1, new_msg1)
            src_msg2 = "The generated query should return all of the information asked in the question without any missing or extra information."
            new_msg2 = "Remember that one of the draft SQLs is correct. You do not need to generate a new SQL combining their characteristics. Instead, output the draft SQL that you think is correct after careful analysis."
            question_raw = question_raw.replace(src_msg2, new_msg2)

        return question_raw

    question_raw = dp[instruction_key]
    if other_input:
        question_raw += other_input
    task_msg = "Please output only the final SQL query, starts with keyword `SELECT`."

    question_raw = question_raw.replace(task_msg, '')

    if template_type == 'ddl':
        """This works for any base model"""
        omni_output_format = """Output Format:\nIn your answer, please enclose the generated SQL query in a code block:\n```sql\n-- Your SQL query\n```\n\nTake a deep breath and think step by step to find the correct SQL query.\n"""
        question_raw = question_raw.replace(omni_output_format, '')

        prefix = f"""You first thinks about the reasoning process in the mind and then provides the user with the answer.\n\
{question_raw}

Output Format:
Return the final SQLite SQL query that starts with keyword `SELECT` in <answer> </answer> tags, \
for example <answer>SELECT AVG(rating_score) FROM movies</answer>. \
Let me solve this step by step."""
    elif template_type == 'think':
        omni_output_format = """Output Format:\nIn your answer, please enclose the generated SQL query in a code block:\n```sql\n-- Your SQL query\n```\n\nTake a deep breath and think step by step to find the correct SQL query.\n"""
        question_raw = question_raw.replace(omni_output_format, '')

        prefix = f"""You first thinks about the reasoning process in the mind and then provides the user with the answer.\n\
{question_raw}

Output Format:
Show your work in <think> </think> tags. And return the final SQLite SQL query that starts with keyword `SELECT` in <answer> </answer> tags, \
for example <answer>SELECT AVG(rating_score) FROM movies</answer>. \

Let me solve this step by step."""
    else:
        prefix = dp[instruction_key]
        if other_input:
            prefix += other_input

    return prefix


# Format into conversation
def make_map_fn(split, dataset_name="bird", template_name="think"):
    def process_fn(example: Dict, idx):
        prompt = []

        if training_args.system_prompt is not None:
            prompt.append({"role": "system", "content": training_args.system_prompt})

        instruction = make_prefix(example, template_type=template_name)
        prompt.append({"role": "user", "content": instruction})

        sql = example["output"]
        question_id = example["id"]
        db_id = example["db_id"]

        if isinstance(sql, dict):
            sql = get_predict_columns_from_schema(sql)

        ground_truth = {
            "dataset_name": dataset_name,
            "split": split,
            'question_id': question_id,
            "db_id": db_id,
            "sql": sql,
        }

        result = {
            "prompt": prompt,
            "ground_truth": ground_truth
        }

        return result

    return process_fn


class GRPOTrainer2(GRPOTrainer):

    def _save_checkpoint(self, model, trial):
        # In all cases, including ddp/dp/deepspeed, self.model is always a reference to the model we
        # want to save except FullyShardedDDP.
        # assert unwrap_model(model) is self.model, "internal model should be a reference to self.model"

        # Save model checkpoint
        checkpoint_folder = f"{PREFIX_CHECKPOINT_DIR}-{self.state.global_step}"

        if self.hp_search_backend is None and trial is None:
            self.store_flos()

        run_dir = self._get_output_dir(trial=trial)
        output_dir = os.path.join(run_dir, checkpoint_folder)
        self.save_model(output_dir, _internal_call=True)

        if not self.args.save_only_model:
            # Save optimizer and scheduler
            self._save_optimizer_and_scheduler(output_dir)
            self._save_scaler(output_dir)
            # Save RNG state
            self._save_rng_state(output_dir)

        # Save the Trainer state
        if self.args.should_save:
            # Update `ExportableState` callbacks and `TrainerControl` state to where we are currently
            for cb in [
                cb for cb in self.callback_handler.callbacks + [self.control] if isinstance(cb, ExportableState)
            ]:
                cb_name = cb.__class__.__name__
                cb_state = cb.state()

                if isinstance(self.state.stateful_callbacks[cb_name], list):
                    self.state.stateful_callbacks[cb_name].append(cb_state)
                else:
                    self.state.stateful_callbacks[cb_name] = cb_state
            try:
                save_json_path = os.path.join(output_dir, TRAINER_STATE_NAME)
                state_data = dataclasses.asdict(self.state)
                new_data = {}
                for k, v in state_data.items():
                    if k == 'learning_rate' or isinstance(v, torch.Tensor):
                        new_data[k] = v.tolist()
                    else:
                        new_data[k] = v
                json_string = json.dumps(new_data, indent=2, sort_keys=True) + "\n"
                with open(save_json_path, "w", encoding="utf-8") as f:
                    f.write(json_string)
                with open(save_json_path.replace(".json", ".txt"), "w", encoding='utf-8') as f:
                    f.writelines(str(state_data))

                # self.state.save_to_json(os.path.join(output_dir, TRAINER_STATE_NAME))
            except Exception as e:
                logger.warning(f"save state error: {e}")

        if self.args.push_to_hub:
            self._push_from_checkpoint(output_dir)

        # Maybe delete some older checkpoints.
        if self.args.should_save:
            # Solely rely on numerical checkpoint id for rotation.
            # mtime is not reliable especially on some fuse fs in cloud environments.
            self._rotate_checkpoints(use_mtime=False, output_dir=run_dir)


def get_reward_funcs(script_args: GRPOScriptArguments) -> list[Callable]:
    REWARD_FUNCS_REGISTRY = {
        # "accuracy": accuracy_reward,
        "execute_accuracy": execute_accuracy_reward,
        "selection_vote": selection_vote_reward,
        "link_table": link_table_reward,
        "link_column": link_column_reward,
        "link_column_from_sql": link_column_from_sql_reward,
        "format": format_reward,
        # "reasoning_steps": reasoning_steps_reward,
        # "cosine": get_cosine_scaled_reward(
        #     min_value_wrong=script_args.cosine_min_value_wrong,
        #     max_value_wrong=script_args.cosine_max_value_wrong,
        #     min_value_correct=script_args.cosine_min_value_correct,
        #     max_value_correct=script_args.cosine_max_value_correct,
        #     max_len=script_args.cosine_max_len,
        # ),
        # "repetition_penalty": get_repetition_penalty_reward(
        #     ngram_size=script_args.repetition_n_grams,
        #     max_penalty=script_args.repetition_max_penalty,
        # ),
        # "length": len_reward,
        # "code": code_reward,
        # "code_format": get_code_format_reward(language=script_args.code_language),
        # "tag_count": tag_count_reward,
    }
    reward_funcs = [REWARD_FUNCS_REGISTRY[func] for func in script_args.reward_funcs]

    return reward_funcs


def main(script_args: GRPOScriptArguments, training_args: GRPOConfig, model_args: ModelConfig):
    # Set seed for reproducibility
    set_seed(training_args.seed)

    ###############
    # Setup logging
    ###############
    logging.basicConfig(
        format="%(asctime)s - %(levelname)s - %(name)s - %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
        handlers=[logging.StreamHandler(sys.stdout)],
    )
    log_level = training_args.get_process_log_level()
    logger.setLevel(log_level)
    datasets.utils.logging.set_verbosity(log_level)
    transformers.utils.logging.set_verbosity(log_level)
    transformers.utils.logging.enable_default_handler()
    transformers.utils.logging.enable_explicit_format()

    # Log on each process a small summary
    logger.warning(
        f"Process rank: {training_args.local_rank}, device: {training_args.device}, n_gpu: {training_args.n_gpu}"
        + f" distributed training: {bool(training_args.local_rank != -1)}, 16-bits training: {training_args.fp16}"
    )
    logger.info(f"Model parameters {model_args}")
    logger.info(f"Script parameters {script_args}")
    logger.info(f"Training parameters {training_args}")

    # Check for last checkpoint
    last_checkpoint = None
    if os.path.isdir(training_args.output_dir):
        last_checkpoint = get_last_checkpoint(training_args.output_dir)
    if last_checkpoint is not None and training_args.resume_from_checkpoint is None:
        logger.info(f"Checkpoint detected, resuming training at {last_checkpoint=}.")

    if "wandb" in training_args.report_to:
        init_wandb_training(training_args)

    # Load the dataset
    do_eval = training_args.do_eval
    dataset_name = script_args.dataset_name
    data_files = {"train": script_args.dataset_path}

    if do_eval:
        if dataset_name == "bird":
            script_args.dataset_test_split = "dev"
        eval_split = script_args.dataset_test_split
        if eval_split in ["dev", "test"]:
            dev_data_files = script_args.dataset_path.replace('train.json', f'{eval_split}.json')
            if os.path.exists(dev_data_files):
                data_files[eval_split] = dev_data_files

    # dataset = load_dataset(script_args.dataset_name, name=script_args.dataset_config)
    dataset = load_dataset("json", data_files=data_files)

    ################
    # Load tokenizer
    ################
    tokenizer = get_tokenizer(model_args, training_args)

    ##############
    # Load model #
    ##############
    logger.info("*** Loading model ***")
    model = get_model(model_args, training_args)

    # Get reward functions
    reward_funcs = get_reward_funcs(script_args)

    train_dataset = dataset["train"]
    train_dataset = train_dataset.map(
        function=make_map_fn("train", dataset_name=dataset_name, template_name=script_args.template_name),
        with_indices=True)

    src_total = len(train_dataset)
    train_dataset = [item for item in train_dataset if
                     len(item['prompt'][-1]['content']) < script_args.max_train_prompt_len]
    clip_total = len(train_dataset)
    print(f"filter train total: {src_total - clip_total} = {src_total} - {clip_total}")
    dataset["train"] = train_dataset

    if do_eval:
        eval_dataset = dataset[eval_split]
        eval_dataset = eval_dataset.map(
            function=make_map_fn(eval_split, dataset_name=dataset_name, template_name=script_args.template_name),
            with_indices=True)

        eval_dataset = [item for item in eval_dataset if
                        len(item['prompt'][-1]['content']) < script_args.max_train_prompt_len]

        dataset[eval_split] = eval_dataset

    print(f"len train: {len(train_dataset)}")
    print("prompt[0]")
    print(train_dataset[0]["prompt"][0]['content'] + train_dataset[0]["prompt"][1]['content'])

    #############################
    # Initialize the GRPO trainer
    #############################
    trainer = GRPOTrainer2(
        model=model,
        reward_funcs=reward_funcs,
        args=training_args,
        train_dataset=dataset[script_args.dataset_train_split],
        eval_dataset=dataset[script_args.dataset_test_split] if training_args.eval_strategy != "no" else None,
        peft_config=get_peft_config(model_args),
        callbacks=get_callbacks(training_args, model_args),
        processing_class=tokenizer,
    )

    ###############
    # Training loop
    ###############
    logger.info("*** Train ***")
    checkpoint = None
    # if training_args.resume_from_checkpoint is not None:
    #     checkpoint = training_args.resume_from_checkpoint
    # elif last_checkpoint is not None:
    #     checkpoint = last_checkpoint
    train_result = trainer.train(resume_from_checkpoint=checkpoint)
    metrics = train_result.metrics
    metrics["train_samples"] = len(dataset[script_args.dataset_train_split])
    trainer.log_metrics("train", metrics)
    trainer.save_metrics("train", metrics)
    try:
        trainer.save_state()
    except Exception as e:
        logger.warning(f"save state error: {e}")

    ##################################
    # Save model and create model card
    ##################################
    logger.info("*** Save model ***")
    trainer.save_model(training_args.output_dir)
    logger.info(f"Model saved to {training_args.output_dir}")

    # Save everything else on main process
    kwargs = {
        "dataset_name": script_args.dataset_name,
        # "data_files": data_files,
        "tags": ["open-r1"],
    }
    if trainer.accelerator.is_main_process:
        trainer.create_model_card(**kwargs)
        # Restore k,v cache for fast inference
        trainer.model.config.use_cache = True
        trainer.model.config.save_pretrained(training_args.output_dir)

    ##########
    # Evaluate
    ##########
    if training_args.do_eval:
        logger.info("*** Evaluate ***")
        metrics = trainer.evaluate()
        metrics["eval_samples"] = len(dataset[script_args.dataset_test_split])
        trainer.log_metrics("eval", metrics)
        trainer.save_metrics("eval", metrics)

    #############
    # push to hub
    #############
    if training_args.push_to_hub:
        logger.info("Pushing to hub...")
        trainer.push_to_hub(**kwargs)


if __name__ == "__main__":
    parser = TrlParser((GRPOScriptArguments, GRPOConfig, ModelConfig))
    script_args, training_args, model_args = parser.parse_args_and_config()
    main(script_args, training_args, model_args)

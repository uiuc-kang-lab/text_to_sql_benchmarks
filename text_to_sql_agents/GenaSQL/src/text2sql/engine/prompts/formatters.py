import datetime
import json

from abc import ABC, abstractmethod

from text2sql.engine.prompts.constants_v3 import (
    GENA_MYSQL_GUIDELINES,
    GENA_POSTGRES_GUIDELINES,
    GENA_SQLITE_GUIDELINES,
    GENA_USER_QUERY_EVIDENCE_SCHEMA_TEMPLATE,
    GENA_COT_W_EVIDENCE_PROMPT_TEMPLATE,
    GENA_ASSISTANT_TEMPLATE,
    REWRITE_PROMPT_TEMPLATE,
    REWRITE_USER_MESSAGE_TEMPLATE,
    GENA_USER_QUERY_SCHEMA_TEMPLATE,
)

from text2sql.engine.prompts.constants_schema_linking import (
    SCHEMA_LINKING_SYSTEM_PROMPT,
    SCHEMA_LINKING_EXAMPLE_PROMPT_TEMPLATE,
    SCHEMA_LINKING_USER_PROMPT_TEMPLATE,
)


class BasePromptFormatter(ABC):

    @abstractmethod
    def generate_messages(self, query: str) -> list[dict]:
        pass


class GenaCoTwEvidencePromptFormatter(BasePromptFormatter):
    """format messages in the GENA AI API format with custom prompt template."""

    def __init__(
        self,
        database_type: str,
        few_shot_query_key: str = "nl_en_query",
        few_shot_target_key: str = "sql_query",
        fewshot_schema_key: str | None = None,
    ):
        self.database_type = database_type
        self.few_shot_query_key = few_shot_query_key
        self.few_shot_target_key = few_shot_target_key
        self.fewshot_schema_key = fewshot_schema_key

    def generate_messages(
        self,
        schema_description: str,
        query: str,
        evidence: str,
        few_shot_examples: list[dict] = [],
    ) -> list[dict]:
        if self.database_type == "mysql":
            dialect_guidelines = GENA_MYSQL_GUIDELINES
        elif self.database_type == "postgres":
            dialect_guidelines = GENA_POSTGRES_GUIDELINES
        elif self.database_type == "sqlite":
            dialect_guidelines = GENA_SQLITE_GUIDELINES
        else:
            raise ValueError(f"unsupported database type: {self.database_type}")

        formatted_system_message = GENA_COT_W_EVIDENCE_PROMPT_TEMPLATE.format(
            sql_dialect=self.database_type,
            dialect_guidelines=dialect_guidelines,
            # schema_description=schema_description
        )
        messages = [{"role": "system", "content": formatted_system_message}]

        if few_shot_examples and self.fewshot_schema_key is None:
            raise ValueError("fewshot_schema_key is not provided")

        for example in few_shot_examples:
            example_query = example["data"][self.few_shot_query_key]
            example_sql = example["data"][self.few_shot_target_key]
            example_desc = example["data"][self.fewshot_schema_key]
            if "evidence" in example["data"]:
                example_evidence = example["data"]["evidence"]
                messages.append(
                    {
                        "role": "user",
                        "content": GENA_USER_QUERY_EVIDENCE_SCHEMA_TEMPLATE.format(
                            schema_description=example_desc,
                            user_question=example_query,
                            evidence=example_evidence,
                            sql_dialect=self.database_type,
                        ),
                    }
                )
            else:
                messages.append(
                    {
                        "role": "user",
                        "content": GENA_USER_QUERY_SCHEMA_TEMPLATE.format(
                            schema_description=example_desc, user_question=example_query, sql_dialect=self.database_type
                        ),
                    }
                )
            messages.append({"role": "assistant", "content": GENA_ASSISTANT_TEMPLATE.format(sql_query=example_sql)})

        query_message = GENA_USER_QUERY_EVIDENCE_SCHEMA_TEMPLATE.format(
            schema_description=schema_description,
            user_question=query,
            evidence=evidence,
            sql_dialect=self.database_type,
        )

        messages.append({"role": "user", "content": query_message})
        return messages


class RewritePromptFormatter(BasePromptFormatter):
    """format messages for rewrite with custom prompt template."""

    def __init__(
        self,
        database_type: str,
    ):
        self.database_type = database_type

    def generate_messages(
        self,
        schema_description: str,
        query: str,
        predicted_sql: str,
    ) -> list[dict]:

        formatted_system_message = REWRITE_PROMPT_TEMPLATE.format(sql_dialect=self.database_type)
        messages = [{"role": "system", "content": formatted_system_message}]

        query_message = REWRITE_USER_MESSAGE_TEMPLATE.format(
            schema_description=schema_description,
            #  relevant_tables=table_text,
            user_question=query,
            original_sql=predicted_sql,
        )
        messages.append({"role": "user", "content": query_message})
        return messages


class SchemaLinkingFewShotFormatter:
    """format schema linking messages with few-shot examples."""

    def __init__(
        self,
        schema_linking_examples: list[dict],
        description_format: str,
    ):
        self.system_prompt = SCHEMA_LINKING_SYSTEM_PROMPT
        for example in schema_linking_examples:
            if description_format in example["schema_descriptions"]:
                example_description: str = example["schema_descriptions"][description_format]
            else:
                default_key = sorted(list(example["schema_descriptions"].keys()))[0]
                example_description: str = example["schema_descriptions"][default_key]
            example_question: str = example["question"]
            example_evidence: str = example["evidence"]
            example_answer: dict = example["answer"]
            self.system_prompt += SCHEMA_LINKING_EXAMPLE_PROMPT_TEMPLATE.format(
                example_description=example_description,
                example_question=example_question,
                example_evidence=example_evidence,
                example_answer=json.dumps(example_answer, ensure_ascii=False, indent=2),
            )

    def generate_messages(
        self,
        schema_description: str,
        question: str,
        evidence: str,
        gemini: bool = False,
    ) -> list[dict]:
        messages = [{"role": "system", "content": self.system_prompt}]

        query_message = SCHEMA_LINKING_USER_PROMPT_TEMPLATE.format(
            schema_description=schema_description,
            question=question,
            evidence=evidence,
        )
        if gemini:
            query_message += " Use double quotes for keys and values in the JSON output."

        messages.append({"role": "user", "content": query_message})
        return messages

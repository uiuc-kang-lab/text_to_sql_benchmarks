import time

from abc import ABC, abstractmethod
from typing import Callable

import google.generativeai as genai_legacy

from google import genai
from google.genai import types
from openai import AzureOpenAI, OpenAI
from pydantic import BaseModel
from tenacity import retry, wait_random_exponential, stop_after_attempt

from text2sql.engine.clients import get_azure_client, get_bedrock_client, get_openai_client
from text2sql.engine.generation.converters import convert_messages_to_bedrock_format


def identity(x: str) -> str:
    return x


STATUS_OK = "ok"


class TokenUsage(BaseModel):
    """token usage for a single generation call"""

    cached_tokens: int = 0
    prompt_tokens: int
    output_tokens: int
    reasoning_tokens: int = 0  # for backwards compatibility
    total_tokens: int
    inf_time_ms: int

    # allow adding two TokenUsages
    def __add__(self, other: "TokenUsage") -> "TokenUsage":
        return TokenUsage(
            cached_tokens=self.cached_tokens + other.cached_tokens,
            prompt_tokens=self.prompt_tokens + other.prompt_tokens,
            output_tokens=self.output_tokens + other.output_tokens,
            reasoning_tokens=self.reasoning_tokens + other.reasoning_tokens,
            total_tokens=self.total_tokens + other.total_tokens,
            inf_time_ms=self.inf_time_ms + other.inf_time_ms,
        )


class GenerationResult(BaseModel):
    """result of a single generation call"""

    model: str
    text: str
    tokens: TokenUsage
    status: str = STATUS_OK


class BaseGenerator(ABC):
    @abstractmethod
    def generate(self, messages: list[dict], **kwargs) -> str:
        pass


class AzureGenerator(BaseGenerator):

    def __init__(
        self,
        api_key: str,
        api_version: str,
        azure_endpoint: str,
        model: str,
        post_func: Callable[[str], str] = identity,
        **kwargs,
    ):
        """generate text using Azure OpenAI API

        Args:
            api_key (str): azure api key
            api_version (str): azure api version (mm-dd-yyyy)
            azure_endpoint (str): azure endpoint url
            model (str): azure model deployment name
            kwargs: additional azure client specific arguments

        """
        self.api_key = api_key
        self.api_version = api_version
        self.azure_endpoint = azure_endpoint
        self.model = model
        self.post_func = post_func
        self.client: AzureOpenAI = get_azure_client(
            api_key=self.api_key, api_version=self.api_version, azure_endpoint=self.azure_endpoint, **kwargs
        )

    @retry(wait=wait_random_exponential(min=5, max=60), stop=stop_after_attempt(8))
    def generate(self, messages: list[dict], **kwargs) -> GenerationResult:
        """embed one batch of texts with azure"""

        # run inference
        start_time = time.time()
        chat_completion = self.client.chat.completions.create(model=self.model, messages=messages, **kwargs)
        end_time = time.time()

        # as of 4.19.2025, the OpenAI API REST API uses "input_tokens" and "output_tokens"
        # ref: https://platform.openai.com/docs/api-reference/responses/get
        # however, as of version 1.61.1, the python openai client uses "prompt_tokens" and "completion_tokens" with azure
        # tested with API version "2024-10-21" and "2024-12-01-preview" with both gpt-4o-mini and o3-mini
        # in case of potential future changes, try to use the current names, but if attr not exist, use the new names

        # get prompt (input) token usage, support prompt_tokens as well as input_tokens (new api?)
        if hasattr(chat_completion.usage, "prompt_tokens"):
            prompt_tokens = chat_completion.usage.prompt_tokens
        elif hasattr(chat_completion.usage, "input_tokens"):
            prompt_tokens = chat_completion.usage.input_tokens
        else:
            prompt_tokens = 0

        # get cached input token usage, support new api(?) as well
        if hasattr(chat_completion.usage, "prompt_tokens_details") and hasattr(
            chat_completion.usage.prompt_tokens_details, "cached_tokens"
        ):
            cached_tokens = chat_completion.usage.prompt_tokens_details.cached_tokens
        elif hasattr(chat_completion.usage, "input_tokens_details") and hasattr(
            chat_completion.usage.input_tokens_details, "cached_tokens"
        ):
            cached_tokens = chat_completion.usage.input_tokens_details.cached_tokens
        else:
            cached_tokens = 0

        # get completion (output) token usage, support completion_tokens as well as output_tokens (new api?)
        if hasattr(chat_completion.usage, "completion_tokens"):
            output_tokens = chat_completion.usage.completion_tokens
        elif hasattr(chat_completion.usage, "output_tokens"):
            output_tokens = chat_completion.usage.output_tokens
        else:
            output_tokens = 0

        # support reasoning token usage
        if hasattr(chat_completion.usage, "completion_tokens_details") and hasattr(
            chat_completion.usage.completion_tokens_details, "reasoning_tokens"
        ):
            reasoning_tokens = chat_completion.usage.completion_tokens_details.reasoning_tokens
        elif hasattr(chat_completion.usage, "output_tokens_details") and hasattr(
            chat_completion.usage.output_tokens_details, "reasoning_tokens"
        ):
            reasoning_tokens = chat_completion.usage.output_tokens_details.reasoning_tokens
        else:
            reasoning_tokens = 0

        # postprocessing
        text = self.post_func(chat_completion.choices[0].message.content)
        inf_time_ms = int((end_time - start_time) * 1000)
        token_usage = TokenUsage(
            cached_tokens=cached_tokens,
            prompt_tokens=prompt_tokens,
            output_tokens=output_tokens,
            reasoning_tokens=reasoning_tokens,
            total_tokens=chat_completion.usage.total_tokens,
            inf_time_ms=inf_time_ms,
        )
        return GenerationResult(model=self.model, text=text, tokens=token_usage)


class BedrockGenerator(BaseGenerator):
    def __init__(
        self,
        region_name: str,
        model: str,
        post_func: Callable[[str], str] = identity,
        **kwargs,
    ):
        """generate text using Bedrock API

        Args:
            region_name (str): bedrock region name
            model (str): bedrock model name
            kwargs: additional azure client specific arguments
        """
        self.region_name = region_name
        self.model = model
        self.post_func = post_func
        self.client = get_bedrock_client(region_name=self.region_name, **kwargs)

    @retry(wait=wait_random_exponential(min=5, max=60), stop=stop_after_attempt(8))
    def generate(self, messages: list[dict], **kwargs) -> GenerationResult:
        # format to nested bedrock format & run inference
        system_message, formatted_messages = convert_messages_to_bedrock_format(model=self.model, messages=messages)
        start_time = time.time()
        if system_message:
            response = self.client.converse(
                modelId=self.model,
                system=system_message,
                messages=formatted_messages,
                **kwargs,
            )
        else:
            response = self.client.converse(
                modelId=self.model,
                messages=formatted_messages,
                **kwargs,
            )
        end_time = time.time()

        # get token usage
        cached_tokens = response["usage"]["cachedReadInputTokens"]
        if cached_tokens is None:
            cached_tokens = 0
        token_usage = TokenUsage(
            cached_tokens=cached_tokens,
            prompt_tokens=response["usage"]["inputTokens"],
            output_tokens=response["usage"]["outputTokens"],
            total_tokens=response["usage"]["totalTokens"],
            inf_time_ms=int((end_time - start_time) * 1000),
        )

        return GenerationResult(
            model=self.model,
            text=self.post_func(response["output"]["message"]["content"][-1]["text"]),
            tokens=token_usage,
        )


class GCPGenerator(BaseGenerator):

    def __init__(
        self,
        api_key: str,
        model: str,
        post_func: Callable[[str], str] = identity,
    ):
        """generate text using GCP API

        Args:
            api_key (str): gcp api key
            model (str): gemini model name
            kwargs: additional gemini specific arguments

        """
        self.model = model
        self.post_func = post_func
        self.client = genai.Client(api_key=api_key)
        self.history = []

    @retry(wait=wait_random_exponential(min=3, max=30), stop=stop_after_attempt(3))
    def generate(self, messages: list[dict], **kwargs) -> GenerationResult:

        # create config depending on system prompt
        system_instruction = "\n".join([message["content"] for message in messages if message["role"] == "system"])
        if system_instruction:
            config = types.GenerateContentConfig(system_instruction=system_instruction, **kwargs)
        else:
            config = types.GenerateContentConfig(**kwargs)

        # format messages to GCP format
        history = []
        for message in messages[:-1]:
            # new API uses "model" instead of "assistant" for all models
            if message["role"] in ["assistant", "user"]:
                if message["role"] == "assistant":
                    role = "model"
                else:
                    role = "user"
                message = {"role": role, "parts": [{"text": message["content"]}]}
                history.append(message)

        # set model, history in the create method
        chat = self.client.chats.create(
            model=self.model,
            config=config,
            history=history,
        )

        # run inference
        start_time = time.time()
        # run inference with text input
        result: types.GenerateContentResponse = chat.send_message(messages[-1]["content"])
        end_time = time.time()

        # get token usage
        if hasattr(result, "usage_metadata"):
            cached_tokens = result.usage_metadata.cached_content_token_count
            cached_tokens = 0 if cached_tokens is None else cached_tokens
            prompt_tokens = result.usage_metadata.prompt_token_count
            prompt_tokens = 0 if prompt_tokens is None else prompt_tokens
            reasoning_tokens = result.usage_metadata.thoughts_token_count
            reasoning_tokens = 0 if reasoning_tokens is None else reasoning_tokens
            output_tokens = result.usage_metadata.candidates_token_count
            output_tokens = 0 if output_tokens is None else output_tokens
            total_tokens = result.usage_metadata.total_token_count
            total_tokens = 0 if total_tokens is None else total_tokens
            status = STATUS_OK
        else:
            cached_tokens = 0
            prompt_tokens = 0
            output_tokens = 0
            total_tokens = 0
            status = "error: no usage metadata"
        token_usage = TokenUsage(
            cached_tokens=cached_tokens,
            prompt_tokens=prompt_tokens,
            reasoning_tokens=reasoning_tokens,
            output_tokens=output_tokens,
            total_tokens=total_tokens,
            inf_time_ms=int((end_time - start_time) * 1000),
        )
        self.history = chat.get_history()
        return GenerationResult(
            model=self.model,
            text=self.post_func(result.text),
            tokens=token_usage,
            status=status,
        )


class LegacyGCPGenerator(BaseGenerator):

    def __init__(
        self,
        api_key: str,
        model: str,
        post_func: Callable[[str], str] = identity,
    ):
        """generate text using GCP API

        Args:
            api_key (str): gcp api key
            model (str): gemini model name
            kwargs: additional gemini specific arguments

        """
        self.model = model
        self.post_func = post_func
        self.history = []
        genai_legacy.configure(api_key=api_key)

    @retry(wait=wait_random_exponential(min=3, max=30), stop=stop_after_attempt(3))
    def generate(self, messages: list[dict], **kwargs) -> GenerationResult:
        # create client depending on system prompt
        system_instruction = "\n".join([message["content"] for message in messages if message["role"] == "system"])
        if system_instruction:
            client = genai_legacy.GenerativeModel(
                self.model,
                system_instruction=system_instruction,
                generation_config=kwargs,
            )
        else:
            client = genai_legacy.GenerativeModel(
                self.model,
                generation_config=kwargs,
            )
        # format messages to GCP format
        history = []
        for message in messages[:-1]:
            if message["role"] in ["assistant", "user"]:
                if "content" not in message:
                    print(f"{message=}")
                new_message = {"role": message["role"], "parts": message["content"]}
                history.append(new_message)

        # run inference
        start_time = time.time()
        chat = client.start_chat(history=history)
        result = chat.send_message(messages[-1]["content"])
        end_time = time.time()

        # get token usage
        if hasattr(result, "usage_metadata"):
            cached_tokens = result.usage_metadata.cached_content_token_count
            prompt_tokens = result.usage_metadata.prompt_token_count
            output_tokens = result.usage_metadata.candidates_token_count
            total_tokens = result.usage_metadata.total_token_count
            status = STATUS_OK
        else:
            cached_tokens = 0
            prompt_tokens = 0
            output_tokens = 0
            total_tokens = 0
            status = "error: no usage metadata"
        token_usage = TokenUsage(
            cached_tokens=cached_tokens,
            prompt_tokens=prompt_tokens,
            output_tokens=output_tokens,
            total_tokens=total_tokens,
            inf_time_ms=int((end_time - start_time) * 1000),
        )
        self.history = chat.history
        return GenerationResult(
            model=self.model,
            text=self.post_func(result.text),
            tokens=token_usage,
            status=status,
        )


class OpenAIGenerator(BaseGenerator):

    def __init__(
        self,
        api_key: str,
        model: str,
        post_func: Callable[[str], str] = identity,
        base_url: str | None = None,
        **kwargs,
    ):
        """generate text using OpenAI client
        can be used for DeepSeek as well

        Args:
            api_key (str): api key for OpenAI or DeepSeek
            model (str): model identifier
            base_url (str): base url for API calls
            kwargs: additional openai client specific arguments

        """
        self.model = model
        self.post_func = post_func
        self.client: OpenAI = get_openai_client(api_key=api_key, base_url=base_url, **kwargs)

    @retry(wait=wait_random_exponential(min=5, max=60), stop=stop_after_attempt(8))
    def generate(self, messages: list[dict], **kwargs) -> GenerationResult:
        """embed one batch of texts with azure"""

        # run inference
        start_time = time.time()
        chat_completion = self.client.chat.completions.create(model=self.model, messages=messages, **kwargs)
        end_time = time.time()

        # get token usage
        if hasattr(chat_completion.usage, "prompt_tokens_details") and hasattr(
            chat_completion.usage.prompt_tokens_details, "cached_tokens"
        ):
            cached_tokens = chat_completion.usage.prompt_tokens_details.cached_tokens
        else:
            cached_tokens = 0

        # postprocessing
        text = self.post_func(chat_completion.choices[0].message.content)

        token_usage = TokenUsage(
            cached_tokens=cached_tokens,
            prompt_tokens=chat_completion.usage.prompt_tokens,
            output_tokens=chat_completion.usage.completion_tokens,
            total_tokens=chat_completion.usage.total_tokens,
            inf_time_ms=int((end_time - start_time) * 1000),
        )

        return GenerationResult(model=self.model, text=text, tokens=token_usage)

from abc import ABC, abstractmethod

import json
import time
import tqdm

from loguru import logger
from openai import OpenAI, AzureOpenAI
from pydantic import BaseModel
from tenacity import retry, wait_random_exponential, stop_after_attempt

from text2sql.engine.clients import get_openai_client, get_azure_client, get_bedrock_client


class EmbeddingResult(BaseModel):
    """result of a single embedding call"""

    texts: list[str]
    embeddings: list[list[float]]
    input_characters: int
    inf_time_ms: int


class BaseEmbedder(ABC):
    def __init__(
        self,
        batch_size: int = 8,
        max_chars: int = 1024,
        sleep_ms: int = 0,
    ):
        self.batch_size = batch_size
        self.max_chars = max_chars
        self.sleep_ms: int = sleep_ms

    @abstractmethod
    def _embed_batch(self, batch_samples: list[str]) -> list[list[float]]:
        """batch embedding function for specific client"""
        pass

    def embed_list(self, samples: list[str], verbose: bool = False) -> EmbeddingResult:
        """embed a list of texts, with optional progress bar"""
        character_count: int = 0
        inf_time_ms: int = 0
        input_texts: list[str] = []
        embeddings: list[list[float]] = []
        iter_list = range(0, len(samples), self.batch_size)
        if verbose:
            iter_list = tqdm.tqdm(iter_list)
        for i in iter_list:
            batch_inputs = [text[: self.max_chars] for text in samples[i : i + self.batch_size]]
            input_texts.extend(batch_inputs)
            character_count += sum(len(text) for text in batch_inputs)
            start_time = time.time()
            batch_embeddings = self._embed_batch(batch_inputs)
            end_time = time.time()
            embeddings.extend(batch_embeddings)
            inf_time_ms += int((end_time - start_time) * 1000)
            if self.sleep_ms:
                time.sleep(self.sleep_ms / 1000)
        return EmbeddingResult(
            texts=input_texts,
            embeddings=embeddings,
            input_characters=character_count,
            inf_time_ms=inf_time_ms,
        )

    def embed_text(self, text: str) -> EmbeddingResult:
        """embed a single text"""
        texts = [text[: self.max_chars]]
        start_time = time.time()
        embeddings = self._embed_batch(texts)
        end_time = time.time()
        return EmbeddingResult(
            texts=texts,
            embeddings=embeddings,
            input_characters=len(text[: self.max_chars]),
            inf_time_ms=int((end_time - start_time) * 1000),
        )

    def embed(self, data: str | list[str], verbose: bool = False) -> EmbeddingResult:
        """lazy function to embed either a single text or a list of texts"""
        if isinstance(data, str):
            return self.embed_text(data)
        else:
            return self.embed_list(data, verbose=verbose)


class AzureEmbedder(BaseEmbedder):

    def __init__(
        self,
        api_key: str,
        api_version: str,
        azure_endpoint: str,
        model: str,
        batch_size: int = 8,
        max_chars: int = 1024,
        sleep_ms: int = 0,
        **kwargs,
    ):
        """embed texts using Azure OpenAI API

        Args:
            api_key (str): azure api key
            api_version (str): azure api version (mm-dd-yyyy)
            azure_endpoint (str): azure endpoint url
            model (str): azure model deployment name
            batch_size (int, optional): batch size. Defaults to 8.
            max_chars (int, optional): max chars. Defaults to 1024.
            sleep_ms (int, optional): sleep time in ms. Defaults to 0.
            kwargs: additional azure client specific arguments
        """
        super().__init__(batch_size=batch_size, max_chars=max_chars, sleep_ms=sleep_ms)
        self.api_key = api_key
        self.api_version = api_version
        self.azure_endpoint = azure_endpoint
        self.model = model
        self.client: AzureOpenAI = get_azure_client(
            api_key=self.api_key,
            api_version=self.api_version,
            azure_endpoint=self.azure_endpoint,
            **kwargs,
        )

    @retry(wait=wait_random_exponential(min=5, max=60), stop=stop_after_attempt(8))
    def _embed_batch(self, batch_samples: list[str]) -> list[list[float]]:
        """embed one batch of texts with azure"""
        response = self.client.embeddings.create(
            input=batch_samples,
            model=self.model,
        )
        return [list(x.embedding) for x in response.data]


class OpenAIEmbedder(BaseEmbedder):

    def __init__(
        self,
        api_key: str,
        model: str,
        dimensions: int = 1024,
        batch_size: int = 8,
        max_chars: int = 1024,
        sleep_ms: int = 0,
        **kwargs,
    ):
        """embed texts using OpenAI API

        Args:
            api_key (str): openai api key
            model (str): openai embedding model name
            dimensions (int, optional): embedding dimensions. Defaults to 1024.
            batch_size (int, optional): batch size. Defaults to 8.
            max_chars (int, optional): max chars. Defaults to 1024.
            sleep_ms (int, optional): sleep time in ms. Defaults to 0.
            kwargs: additional openai client specific arguments
        """
        super().__init__(batch_size=batch_size, max_chars=max_chars, sleep_ms=sleep_ms)
        self.api_key = api_key
        self.model = model
        self.dimensions = dimensions
        self.client: OpenAI = get_openai_client(
            api_key=self.api_key,
            **kwargs,
        )

    @retry(wait=wait_random_exponential(min=5, max=60), stop=stop_after_attempt(8))
    def _embed_batch(self, batch_samples: list[str]) -> list[list[float]]:
        """embed one batch of texts with openai"""
        response = self.client.embeddings.create(
            input=batch_samples,
            model=self.model,
            dimensions=self.dimensions,
        )
        return [list(embedding.embedding) for embedding in response.data]
    

class BedrockCohereEmbedder(BaseEmbedder):

    def __init__(
        self,
        region_name: str,
        model: str,
        input_type: str,
        embedding_type: str = "float",
        service_name: str = "bedrock-runtime",
        batch_size: int = 8,
        max_chars: int = 1024,
        sleep_ms: int = 0,
    ):
        """embed texts using Cohere embeddings on Amazon Bedrock API

        Args:
            region_name (str): aws region name
            model (str): bedrock model id
            input_type (str): input type
            embedding_type (str, optional): embedding type. Defaults to "float".
            service_name (str, optional): bedrock service name. Defaults to "bedrock-runtime".
            batch_size (int, optional): batch size. Defaults to 8.
            max_chars (int, optional): max chars. Defaults to 1024.
            sleep_ms (int, optional): sleep time in ms. Defaults to 0.
        """
        super().__init__(batch_size=batch_size, max_chars=max_chars, sleep_ms=sleep_ms)
        self.region_name = region_name
        self.service_name = service_name
        self.model = model
        self.input_type = input_type
        self.embedding_type = embedding_type
        self.client = get_bedrock_client(
            service_name=self.service_name,
            region_name=self.region_name,
        )

    @retry(wait=wait_random_exponential(min=5, max=60), stop=stop_after_attempt(8))
    def _embed_batch(self, batch_samples: list[str]) -> list[list[float]]:
        """embed one batch of texts"""
        request_body = json.dumps(
            {
                "texts": batch_samples,
                "input_type": self.input_type,
                "embedding_types": [self.embedding_type],
            }
        )
        response = self.client.invoke_model(
            body=request_body,
            modelId=self.model,
            accept="*/*",
            contentType="application/json",
        )
        response_body = json.loads(response.get("body").read())
        embeddings_dict: dict = response_body.get("embeddings")
        embeddings = embeddings_dict.get(self.embedding_type)
        return embeddings

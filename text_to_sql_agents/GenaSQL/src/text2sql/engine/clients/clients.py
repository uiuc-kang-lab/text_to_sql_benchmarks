import boto3

from loguru import logger
from openai import AsyncAzureOpenAI, AzureOpenAI, OpenAI


def get_azure_client(api_key: str, api_version: str, azure_endpoint: str, **kwargs) -> AzureOpenAI:
    """get azure client"""
    client = AzureOpenAI(
        api_key=api_key,
        api_version=api_version,
        azure_endpoint=azure_endpoint,
        **kwargs,
    )
    return client


def get_async_azure_client(api_key: str, api_version: str, azure_endpoint: str) -> AsyncAzureOpenAI:
    """get async azure client"""
    client = AsyncAzureOpenAI(
        api_key=api_key,
        api_version=api_version,
        azure_endpoint=azure_endpoint,
    )
    return client


def get_bedrock_client(region_name: str, service_name: str = "bedrock-runtime") -> boto3.client:
    """get bedrock client"""
    return boto3.client(
        service_name=service_name,
        region_name=region_name,
    )


def get_openai_client(api_key: str, base_url: str | None = None) -> OpenAI:
    """get openai client"""
    # If base_url is None the OpenAI library checks OPENAI_BASE_URL env variable
    # If env variable is not set it defaults to https://api.openai.com/v1
    # Deepseek also uses this client by changing the base_url
    client = OpenAI(
        api_key=api_key,
        base_url=base_url,
    )
    return client

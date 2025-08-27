"""
LLM Interface Module

This module provides a unified interface for making calls to different LLM providers
(OpenAI and Anthropic) with consistent input/output handling and cost tracking.
"""

import os
from typing import Dict, Any, Optional, List
import openai
import anthropic
from openai import OpenAI
from pydantic import BaseModel


class LLMInterface:
    """
    A unified interface for interacting with different LLM providers.
    Supports both OpenAI and Anthropic (Claude) models with consistent
    input/output handling and cost tracking.
    """
    
    def __init__(self, model: str, system_prompt: str, api_key: Optional[str] = None, functions: Optional[List[Dict[str, Any]]] = None):
        """
        Initialize the LLM interface.
        
        Args:
            model (str): Model identifier (e.g., 'gpt-4' or 'claude-3-sonnet-20240229')
            api_key (Optional[str]): API key for the service. If None, will try to get from environment
        """
        self.model = model
        self.is_claude = 'claude' in model.lower()
        
        # Set up API key
        if api_key:
            self.api_key = api_key
        else:
            self.api_key = os.getenv("ANTHROPIC_API_KEY" if self.is_claude else "OPENAI_API_KEY")
            
        if not self.api_key:
            raise ValueError(f"No API key provided for {'Anthropic' if self.is_claude else 'OpenAI'}")
            
        # Initialize client
        if self.is_claude:
            self.client = anthropic.Anthropic(api_key=self.api_key)
        else:
            self.client = OpenAI(api_key=self.api_key)
            
        # Model pricing configuration
        self.MODEL_PRICING = {
            "gpt-4": {
                "input": 3.75/1000,
                "output": 15/1000,
                "cache": 1.875/1000
            },
            'claude-3-opus-20240229': {
                "input": 15/1000,
                "output": 60/1000,
                "cache": 7.5/1000
            },
            'claude-3-sonnet-20240229': {
                "input": 3.7/1000,
                "output": 15/1000,
                "cache": 0.3/1000
            },
            'o4-mini' :{
                "input": 1.1/1000,
                "output": 4.4/1000,
                "cache": 0.275/1000
            },
            'o3' :{
                "input": 10/1000,
                "output": 40/1000,
                "cache": 2.5/1000
            },
        }
        
        self.total_cost = 0.0
        self.messages = [{"role": "system", "content": system_prompt}] 
        self.functions = functions

    
    def calculate_cost(self, input_tokens: int, output_tokens: int, cache_tokens: int = 0) -> float:
        """
        Calculate the cost of an API call based on token usage.
        
        Args:
            input_tokens (int): Number of input tokens
            output_tokens (int): Number of output tokens
            cache_tokens (int): Number of cached tokens (default: 0)
            
        Returns:
            float: Total cost in USD
        """
            
        pricing = self.MODEL_PRICING[self.model]
        
        input_cost = (input_tokens / 1000) * pricing["input"]
        output_cost = (output_tokens / 1000) * pricing["output"]
        cache_cost = (cache_tokens / 1000) * pricing["cache"]
        
        return input_cost + output_cost + cache_cost

    def call(self, 
            message: str,
            max_tokens: int = 1000000,
            temperature: float = 1.0,
            response_format: Optional[BaseModel] = None):
        """
        Make a call to the LLM service.
        
        Args:
            prompt (str): The main prompt/question to send
            system_prompt (Optional[str]): System prompt for context/instruction
            max_tokens (int): Maximum tokens in response (default: 1000000)
            temperature (float): Sampling temperature (default: 1.0)
            
        Returns:
            LLMResponse: Standardized response object
        """
        try:
            if self.is_claude:
                # Make API call
                response = self.client.messages.create(
                    model=self.model,
                    max_tokens=max_tokens,
                    messages=messages,
                    temperature=temperature
                )
                
                # Extract response data
                content = response.content[0].text
                input_tokens = response.usage.input_tokens
                output_tokens = response.usage.output_tokens
                cached_tokens = 0
                
            else:
                # Format messages for OpenAI
                messages = [{"role": "user", "content": message}]
                self.messages.append({"role": "user", "content": message})
                # Make API call
                if self.functions:
                    response = self.client.chat.completions.create(
                        model=self.model,
                        messages=self.messages,
                        functions=self.functions,
                        function_call="auto"
                    )
                else:
                    response = self.client.chat.completions.create(
                        model=self.model,
                        messages=self.messages,
                    )
                # Extract response data
                content = response.choices[0].message
                self.messages.append({"role": "assistant", "content": str(content)})
                    
                input_tokens = response.usage.prompt_tokens
                output_tokens = response.usage.completion_tokens
                cached_tokens = getattr(response.usage, 'cached_tokens', 0)
            
                # Calculate and update cost
                cost = self.calculate_cost(input_tokens, output_tokens, cached_tokens)
                self.total_cost += cost
            return content
            
        except Exception as e:
            raise Exception(f"Error calling {self.model}: {str(e)}")

    def get_total_cost(self) -> float:
        """
        Get the total cost of all API calls made through this interface.
        
        Returns:
            float: Total cost in USD
        """
        return self.total_cost 
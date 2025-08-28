from loguru import logger

MODEL_PRICE_PER_1M_TOKENS = {
    "gpt-4o": {"prompt": 2.5, "completion": 10.0},
    "gpt-4": {"prompt": 2.5, "completion": 10.0},   
    "gpt-4o-mini": {"prompt": 0.15, "completion": 0.6},
    "gpt-3.5-turbo": {"prompt": 0.15, "completion": 0.6},   
    "deepseek-chat": {"prompt": 0.14, "completion": 0.28}
}

class CostRecorder:
    def __init__(self, model: str):
        self.model = model
        self.total_prompt_tokens = 0
        self.total_completion_tokens = 0
        self.total_tokens = 0
        self.total_cost = 0
        if self.model in MODEL_PRICE_PER_1M_TOKENS:
            self.total_cost_per_1m_tokens = MODEL_PRICE_PER_1M_TOKENS[self.model]
        else:
            logger.warning(f"Model {self.model} not supported.")
            self.total_cost_per_1m_tokens = {"prompt": 0, "completion": 0}
            logger.warning(f"Set the cost per 1M tokens to 0 for model {self.model}.")
    
    def update_cost(self, prompt_tokens: int, completion_tokens: int):
        self.total_prompt_tokens += prompt_tokens
        self.total_completion_tokens += completion_tokens
        self.total_tokens += prompt_tokens + completion_tokens
        self.total_cost += (prompt_tokens / 1e6 * self.total_cost_per_1m_tokens["prompt"]) + (completion_tokens / 1e6 * self.total_cost_per_1m_tokens["completion"])

    def get_total_prompt_tokens(self):
        return self.total_prompt_tokens
    
    def get_total_completion_tokens(self):
        return self.total_completion_tokens

    def get_total_tokens(self):
        return self.total_tokens
    
    def get_total_cost(self):
        return self.total_cost
    
    def print_profile(self):
        print("-" * 100)
        print(f"Total prompt tokens: {self.total_prompt_tokens}")
        print(f"Total completion tokens: {self.total_completion_tokens}")
        print(f"Total tokens: {self.total_tokens}")
        print(f"Total cost: {self.total_cost}")
        print("-" * 100)
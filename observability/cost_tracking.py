import logging

logger = logging.getLogger(__name__)

class CostTracker:
    def __init__(self):
        # Extremely simplified cost per 1k tokens for Gemini models (example rates)
        self.rates = {
            "gemini-1.5-flash": {"prompt": 0.000125, "completion": 0.000375},
            "gemini-2.5-flash": {"prompt": 0.000150, "completion": 0.000450},
            "gemini-3-flash": {"prompt": 0.000150, "completion": 0.000450}
        }
        self.total_cost = 0.0

    def calculate_cost(self, model_name: str, prompt_tokens: int, completion_tokens: int) -> float:
        if model_name not in self.rates:
            logger.warning(f"Cost rates for {model_name} not found. Defaulting to 0.")
            return 0.0
            
        rate = self.rates[model_name]
        cost = (prompt_tokens / 1000.0) * rate["prompt"] + (completion_tokens / 1000.0) * rate["completion"]
        self.total_cost += cost
        logger.info(f"Query cost: ${cost:.6f} | Total Session Cost: ${self.total_cost:.6f}")
        return cost

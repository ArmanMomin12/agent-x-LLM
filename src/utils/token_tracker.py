# src/utils/token_tracker.py

import time
from datetime import datetime

class TokenTracker:
    def __init__(self):
        self.total_tokens = 0
        self.total_cost = 0.0
        self.history = []

    def log_usage(self, tokens: int, cost_per_1k_tokens: float = 0.002, model: str = "llama3-70b-8192"):
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        cost = (tokens / 1000) * cost_per_1k_tokens
        self.total_tokens += tokens
        self.total_cost += cost

        entry = {
            "timestamp": timestamp,
            "model": model,
            "tokens_used": tokens,
            "cost": round(cost, 4)
        }
        self.history.append(entry)
        print(f"📊 Token Tracker → +{tokens} tokens | Cost: ${round(cost, 4)} | Model: {model}")

    def get_summary(self):
        return {
            "total_tokens": self.total_tokens,
            "total_cost": round(self.total_cost, 4),
            "history": self.history
        }

    def reset(self):
        self.total_tokens = 0
        self.total_cost = 0.0
        self.history = []



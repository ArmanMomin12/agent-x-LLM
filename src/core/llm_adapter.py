import os
import sys
import requests
from dotenv import load_dotenv
import logging

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))

from src.core.retry_handler import retry_on_exception
from src.utils.token_tracker import TokenTracker

# Load GROQ API key
load_dotenv()
api_key = os.getenv("GROQ_API_KEY")
tracker = TokenTracker()

SUPPORTED_MODEL = "llama-3.1-8b-instant"
# Always use a supported model

@retry_on_exception(
    retries=3,
    delay=2,
    backoff=2,
    allowed_exceptions=(requests.exceptions.RequestException,)
)
def query_llm(prompt: str, temperature: float = 0.3, model: str = SUPPORTED_MODEL, role: str = "system") -> str:
    # Check for empty prompt
    if not prompt.strip():
        raise ValueError("Prompt cannot be empty")

    if not api_key:
        raise KeyError("GROQ_API_KEY is not set. Please define it in your .env file.")

    url = "https://api.groq.com/openai/v1/chat/completions"
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }
    payload = {
        "model": model,
        "messages": [
            {"role": "system", "content": "You are an expert AI assistant for code planning, debugging, and development."},
            {"role": "user", "content": prompt}
        ],
        "temperature": temperature,
        "max_tokens": 1500
    }

    response = requests.post(url, headers=headers, json=payload)

    if response.status_code != 200:
        logging.error(f"HTTP Error {response.status_code}: {response.text}")
        raise requests.exceptions.RequestException(f"HTTP Error {response.status_code}: {response.text}")

    result = response.json()

    # Track tokens safely
    tokens_used = result.get("usage", {}).get("total_tokens", 0)
    tracker.log_usage(tokens_used, cost_per_1k_tokens=0.002)

    # Safe parsing of "choices"
    choices = result.get("choices")
    if not choices:
        logging.error("API response missing 'choices': %s", result)
        raise ValueError("LLM did not return any choices")

    message_content = choices[0].get("message", {}).get("content")
    if not message_content:
        logging.error("First choice missing 'content': %s", result)
        raise ValueError("No content in first choice from LLM response")

    return message_content



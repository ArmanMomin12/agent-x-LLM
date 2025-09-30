import logging
from src.core.llm_adapter import query_llm

logging.basicConfig(level=logging.INFO)

def test_llm(prompt: str):
    if not prompt.strip():
        logging.warning("Skipping empty prompt")
        return

    try:
        response = query_llm(prompt)
        logging.info(f"Plan generated for '{prompt}': {response}")
    except Exception as e:
        logging.error(f"Error querying LLM: {e}")
        logging.warning(f"Failed to generate plan for prompt: '{prompt}'")

if __name__ == "__main__":
    prompts = [
        "Build an AI assistant",
        "",  # This will be skipped
        "Credit card fraud detection system"
    ]

    for prompt in prompts:
        test_llm(prompt)



import os
import sys
import requests
from dotenv import load_dotenv
import re
from datetime import datetime

# Ensure project root is in sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))

from src.core.prompt_engine import PromptEngine
from src.core.context_tracker import ContextTracker

# Load API key from .env
load_dotenv()
GROQ_API_KEY = os.getenv("GROQ_API_KEY")

# Initialize prompt engine and context tracker
prompt_engine = PromptEngine()
context = ContextTracker()


def fallback_plan(user_goal: str):
    """
    Return a fallback structured plan if API fails.
    """
    print("⚠️ Using fallback plan.")
    fallback = {
        "goal": user_goal,
        "tasks": [
            "Define requirements",
            "Design architecture",
            "Implement modules",
            "Test and debug",
            "Deploy and monitor"
        ]
    }
    context.update_variable("structured_plan", fallback)
    context.log_event("Fallback plan used", f"Goal: {user_goal}")
    return fallback


def generate_plan(user_goal: str, temperature: float = 0.3, model: str = "llama-3.1-70b-versatile"):
    """
    Generate a structured plan for the given user goal using Groq API.
    Handles errors safely and always returns a structured plan.
    """
    try:
        url = "https://api.groq.com/openai/v1/chat/completions"
        headers = {
            "Authorization": f"Bearer {GROQ_API_KEY}",
            "Content-Type": "application/json"
        }

        # Build prompt
        prompt = prompt_engine.build_planner_prompt(user_goal)

        messages = [
            {
                "role": "system",
                "content": "You are a professional AI software project planner. Break down goals into clear steps."
            },
            {"role": "user", "content": prompt}
        ]

        payload = {
            "model": model,
            "messages": messages,
            "temperature": temperature,
            "max_tokens": 2048
        }

        response = requests.post(url, headers=headers, json=payload)

        # Handle model deprecation errors
        if response.status_code == 400 and "model" in response.text:
            print(f"⚠️ Model {model} not available. Falling back to llama-3.1-8b-instant...")
            payload["model"] = "llama-3.1-8b-instant"
            response = requests.post(url, headers=headers, json=payload)

        if response.status_code != 200:
            print(f"❌ API Error {response.status_code}: {response.text}")
            return fallback_plan(user_goal)

        result = response.json()

        # Safe extraction of choices
        choices = result.get("choices")
        if not choices or len(choices) == 0:
            print("❌ API returned no choices:", result)
            return fallback_plan(user_goal)

        message = choices[0].get("message")
        if not message or "content" not in message:
            print("❌ API choice has no content:", choices[0])
            return fallback_plan(user_goal)

        raw_output = message["content"]
        context.update_variable("raw_llm_output", raw_output)

        # Convert output into structured task list
        task_list = []
        lines = raw_output.strip().split("\n")
        for line in lines:
            match = re.match(r"^\s*(?:\d+\.|-|\*)\s+(.*)", line)
            if match:
                task = match.group(1).strip()
                task_list.append(task)

        # fallback: if nothing parsed, fallback to the whole output as 1 step
        if not task_list:
            task_list = [raw_output.strip()]

        structured_plan = {
            "goal": user_goal,
            "tasks": task_list
        }

        context.update_variable("used_model", model)
        context.update_variable("structured_plan", structured_plan)
        context.log_event("Plan generated", f"Model: {model}")

        return structured_plan

    except Exception as e:
        print("❌ Error generating plan:", e)
        return fallback_plan(user_goal)


# 🔁 Standalone test
if __name__ == "__main__":
    test_goal = "Build an AI assistant that generates, debugs, and deploys Python code."
    plan = generate_plan(test_goal)
    print("✅ Structured Plan:\n", plan)
    print("\n📂 Full Context:\n", context.get_context())

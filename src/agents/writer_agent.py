# src/agents/writer_agent.py

import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))

from src.core.llm_adapter import query_llm  # This should exist
from dotenv import load_dotenv

load_dotenv()

CODE_WRITER_PROMPT = """
You are a professional Python developer.

Generate a clean, modular, and well-documented Python script based on the following project idea:
"""

def write_code(idea: str) -> str:
    prompt = CODE_WRITER_PROMPT + f"\n\n💡 Project Idea:\n{idea}"
    return query_llm(prompt)

if __name__ == "__main__":
    user_idea = input("💡 Enter project idea: ")
    print(write_code(user_idea))



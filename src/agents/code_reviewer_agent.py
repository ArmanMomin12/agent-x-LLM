# src/agents/code_reviewer_agent.py

import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))

from dotenv import load_dotenv
from pathlib import Path
from src.core.llm_adapter import query_llm  # Works with Groq
from typing import Optional

# Load API key from .env
load_dotenv()

def load_code(path: str) -> str:
    if not os.path.exists(path):
        return f"❌ File not found: {path}"
    try:
        with open(path, "r", encoding="utf-8") as f:
            return f.read()
    except Exception as e:
        return f"❌ Error reading file: {e}"

def review_code(path: str) -> str:
    code = load_code(path)
    if code.startswith("❌"):
        return code

    full_prompt = REVIEW_PROMPT + f"\n\n📂 Code:\n```python\n{code}\n```"
    print("📤 Sending code to LLM...")
    response = query_llm(full_prompt)
    print("🧾 LLM response received.")
    return response


REVIEW_PROMPT = """
You are a senior Python software engineer and code reviewer.

Your job is to:
1. Analyze the provided Python code
2. Identify any code smells, bad practices, or inefficient patterns
3. Suggest improvements or refactoring ideas
4. Optionally provide a clean corrected version

Respond in the format below:

1. 🔍 **Code Issues**:
- Issue 1: ...
- Issue 2: ...

2. 💡 **Suggestions**:
- Suggestion 1: ...
- Suggestion 2: ...

3. ✅ **Improved Code** (optional):
```python
# cleaned-up code
"""

if __name__ == "__main__":
    print("🧠 Code Reviewer Agent Started")
    file_path = input("📂 Enter path of Python file to review (e.g., src/agents/self_debugger_agent.py): ").strip()
    report = review_code(file_path)
    
    print("\n📋 Code Review Report:\n")
    print(report)



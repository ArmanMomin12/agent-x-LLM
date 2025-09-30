# src/agents/performance_agent.py

import os
import sys

# Allow root-level imports
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))

from dotenv import load_dotenv
from src.core.llm_adapter import query_llm  # Groq/OpenAI-compatible

load_dotenv()

PERFORMANCE_SYSTEM_PROMPT = """
You are a performance engineering expert.

Please analyze the following Python code and comment on:
- Bottlenecks in execution
- Memory or CPU inefficiencies
- Suggestions for speed or memory optimization
- Any redundant operations

Respond in this format:
1. 🐢 Bottlenecks
2. 💡 Optimization Suggestions
3. ✅ Optional Refactored Snippets (if any)
"""

def run_performance_tests(code: str) -> str:
    print("🚀 Running performance analysis...")
    if not code.strip():
        return "❌ No code provided for performance testing."

    prompt = PERFORMANCE_SYSTEM_PROMPT + f"\n\n```python\n{code}\n```"
    response = query_llm(prompt)
    print("✅ Performance scan completed.")
    return response

# Optional CLI usage
if __name__ == "__main__":
    print("⚙️ Performance Agent Started")
    path = input("📂 Enter Python file to test: ").strip()

    if not os.path.exists(path):
        print("❌ File not found.")
    else:
        with open(path, "r", encoding="utf-8") as f:
            code = f.read()
        report = run_performance_tests(code)
        print("\n📊 Performance Report:\n")
        print(report)



import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))

from dotenv import load_dotenv
from pathlib import Path
from typing import List
from src.core.llm_adapter import query_llm  # Groq-compatible

# ✅ Load environment variables
load_dotenv()

# ✅ Load code from file
def load_code_file(path: str) -> str:
    if not os.path.exists(path):
        return f"❌ File not found: {path}"
    try:
        with open(path, "r", encoding="utf-8") as f:
            return f.read()
    except Exception as e:
        return f"❌ Error reading file: {e}"

# ✅ System Prompt to Debug Code
DEBUG_SYSTEM_PROMPT = """
You are a senior software engineer and code reviewer.

Your job is to find bugs in the provided code and suggest how to fix them. 
Return your analysis in the following format:

1. 🐞 **Bugs Found**: 
- Bug 1: Description
- Bug 2: Description

2. 🛠️ **Suggested Fixes**:
- Fix 1: Description
- Fix 2: Description

3. ✅ **Optional Corrected Code** (if needed):
```python
# corrected code here
```"""

# ✅ Main LLM Debugger Logic (for manual use)
def run_debug_agent(file_path: str) -> str:
    print("📥 Loading file...")
    code = load_code_file(file_path)

    if code.startswith("❌"):
        print("📛 Error loading code")
        return code

    print("📤 Sending to LLM...")
    full_prompt = DEBUG_SYSTEM_PROMPT + f"\n\n📂 Code to debug:\n```python\n{code}\n```"
    result = query_llm(full_prompt)
    print("🧾 LLM response received.")
    return result

# ✅ Required by orchestrator: accepts code string
def debug_code(code: str) -> str:
    print("🧠 Debugging code via LLM...")
    full_prompt = DEBUG_SYSTEM_PROMPT + f"\n\n📂 Code to debug:\n```python\n{code}\n```"
    return query_llm(full_prompt)

# ✅ CLI Entry Point
if __name__ == "__main__":
    print("✅ Self-Debugger Agent Started")
    file_path = input("📂 Enter path of Python file to debug (e.g., src/agents/planner_agent.py): ").strip()
    result = run_debug_agent(file_path)
    print("\n📋 Debug Report:\n")
    print(result)



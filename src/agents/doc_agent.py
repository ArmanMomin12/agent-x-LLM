# src/agents/doc_agent.py

import os
import sys
from dotenv import load_dotenv

# Allow absolute imports from root
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))

from src.core.llm_adapter import query_llm  # Groq-compatible wrapper

# ✅ Load environment variables
load_dotenv()

# ✅ Prompt for documenting Python code
DOC_SYSTEM_PROMPT = """
You are a professional Python developer and technical writer.

You will be provided with raw Python code. Your task is to:

1. Explain what the code does in clear language.
2. Add detailed docstrings to all functions and classes.
3. Ensure the code is still runnable after documentation.

Return only the documented code. Do not summarize it. Keep code formatting clean.
"""

# ✅ Load code from file (used in CLI)
def load_code(file_path: str) -> str:
    if not os.path.exists(file_path):
        return f"❌ File not found: {file_path}"
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            return f.read()
    except Exception as e:
        return f"❌ Error reading file: {e}"

# ✅ Core LLM call with code input (used in orchestrator)
def generate_docs(code: str) -> str:
    """Generate documentation for code (used by orchestrator)."""
    prompt = DOC_SYSTEM_PROMPT + f"\n\n📂 Python Code:\n```python\n{code}\n```"
    return query_llm(prompt)

# ✅ CLI function for file-based use
def run_doc_agent(path: str) -> str:
    print("📥 Loading code...")
    code = load_code(path)
    if code.startswith("❌"):
        return code

    print("📤 Sending to LLM...")
    result = generate_docs(code)
    print("✅ Documentation received.")
    return result

# Add this to the bottom of src/agents/doc_agent.py

def generate_readme_and_gitignore(project_idea: str) -> str:
    prompt = f"""
    You are a software architect.

    Based on the following project idea, generate:
    1. A professional `README.md`
    2. A `.gitignore` file suitable for a Python project

    Respond with both files together, separated clearly.
        
    💡 Project Idea:
    {project_idea}
"""
    return query_llm(prompt)


# ✅ CLI entry point
if __name__ == "__main__":
    print("📚 Documentation Agent Started")
    file_path = input("📂 Enter path of Python file to document (e.g., src/agents/planner_agent.py): ").strip()
    documentation = run_doc_agent(file_path)

    print("\n📝 Documented Code:\n")
    print(documentation)

    # Optional save
    save = input("\n💾 Save documented code to file? (y/n): ").lower()
    if save == "y":
        out_file = input("📁 Enter output filename (e.g., documented_script.py): ").strip()
        try:
            with open(out_file, "w", encoding="utf-8") as f:
                f.write(documentation)
            print(f"✅ Saved to {out_file}")
        except Exception as e:
            print(f"❌ Failed to save: {e}")



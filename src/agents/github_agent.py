import os
import sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))
from dotenv import load_dotenv
from src.core.llm_adapter import query_llm

load_dotenv()

GITHUB_PROMPT = """
You are a GitHub project maintainer and expert in open-source formatting.

Generate the following from a Python project:
1. A professional README.md
2. A relevant .gitignore file
3. Optionally, suggest repo folder structure improvements.

The README should include:
- Project name and description
- Features
- Setup instructions (pip install -r requirements.txt, etc.)
- Run instructions (python main.py)
- Technologies used
- License placeholder
Return all as markdown/text output.
"""

def load_context(path: str) -> str:
    if not os.path.exists(path):
        return "❌ Path does not exist"
    files = os.listdir(path)
    return "Project Directory:\n" + "\n".join(files)

def run_github_agent(path: str):
    print("📁 Loading project context...")
    context = load_context(path)
    prompt = GITHUB_PROMPT + f"\n\n📂 Project Context:\n{context}"
    print("📤 Sending to LLM...")
    result = query_llm(prompt)
    print("✅ GitHub metadata generated.")
    return result

if __name__ == "__main__":
    print("🐙 GitHub Agent Started")
    folder = input("📂 Enter project root folder: ").strip()
    github_docs = run_github_agent(folder)

    print("\n📄 GitHub Files:\n")
    print(github_docs)

    if input("\n💾 Save README.md and .gitignore? (y/n): ").lower() == "y":
        with open("README.md", "w", encoding="utf-8") as f:
            f.write(github_docs.split("```")[0])  # crude separation
        with open(".gitignore", "w", encoding="utf-8") as f:
            f.write("\n".join([
                "__pycache__/",
                "*.pyc",
                ".env",
                "venv/",
                "*.log",
                ".DS_Store"
            ]))
        print("✅ Files saved.")



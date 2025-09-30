# src/agents/docker_agent.py

import os
import sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))
from dotenv import load_dotenv
from src.core.llm_adapter import query_llm

load_dotenv()

# ✅ System Prompt
DOCKER_PROMPT = """
You are a DevOps expert.

Based on the following Python project code or description, generate a clean, production-grade Dockerfile.

The Dockerfile must:
- Use a slim official Python base image
- Set working directory
- Install dependencies using pip and requirements.txt
- Include CMD to run main.py (or the appropriate file)
Return only the Dockerfile, properly formatted.
"""

# ✅ Used internally by CLI or orchestrator
def load_project_overview(path: str) -> str:
    if not os.path.exists(path):
        return f"❌ Path not found: {path}"
    if os.path.isdir(path):
        files = os.listdir(path)
        return f"Project files in {path}:\n" + "\n".join(files)
    with open(path, "r", encoding="utf-8") as f:
        return f.read()

# ✅ Used by CLI
def run_docker_agent(project_path: str):
    print("📦 Analyzing project...")
    content = load_project_overview(project_path)
    if content.startswith("❌"):
        return content
    prompt = DOCKER_PROMPT + f"\n\n📂 Project Code or Structure:\n{content}"
    print("🚢 Sending to LLM...")
    dockerfile = query_llm(prompt)
    print("✅ Dockerfile received.")
    return dockerfile

# ✅ Exported function to orchestrator
def generate_dockerfile(idea, temperature=0.3, model = "llama-3.1-8b-instant"

):
    print(f"[DOCKER AGENT] Generating Dockerfile for idea: {idea}")
    try:
        # your existing logic using query_llm
        response = query_llm(f"Create a Dockerfile for this project:\n{idea}", model=model, temperature=temperature)
        print("[DOCKER AGENT] Response:", response)
        return response.strip()
    except Exception as e:
        print(f"[DOCKER AGENT ERROR] {e}")
        return "FROM python:3.10\n# default fallback Dockerfile"


# ✅ CLI mode
if __name__ == "__main__":
    print("🐳 Dockerfile Generator Agent Started")
    target = input("📁 Enter project directory or entry file (e.g., src/): ").strip()
    output = run_docker_agent(target)

    print("\n📝 Dockerfile:\n")
    print(output)

    if input("\n💾 Save Dockerfile? (y/n): ").lower() == "y":
        with open("Dockerfile", "w", encoding="utf-8") as f:
            f.write(output)
        print("✅ Dockerfile saved.")



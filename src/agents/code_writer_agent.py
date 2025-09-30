# src/agents/code_writer_agent.py

import os
import sys

# Add root project directory to sys.path for absolute imports
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))

from dotenv import load_dotenv
from src.core.llm_adapter import query_llm  # Groq-compatible wrapper

# Load your GROQ_API_KEY from .env
load_dotenv()

# ✅ System Prompt Template
CODE_WRITER_SYSTEM_PROMPT = """
You are a professional Python developer. 

You will be given a user request for a program. Write clean, correct, and well-commented Python code that fulfills the request.

If applicable, split the code into functions, handle edge cases, and write docstrings.
"""

# ✅ Core function to generate code
def run_code_writer(user_prompt: str) -> str:
    print("📤 Generating code from LLM...")
    full_prompt = CODE_WRITER_SYSTEM_PROMPT + f"\n\n📝 User Request:\n{user_prompt}\n\n💻 Write the Python code below:\n"
    result = query_llm(full_prompt)
    print("✅ LLM response received.")
    return result

# ✅ Main runner
if __name__ == "__main__":
    print("🧠 Code Writer Agent Started")
    user_input = input("📌 Describe what you want the code to do: ").strip()
    generated_code = run_code_writer(user_input)
    print("\n💻 Generated Code:\n")
    print(generated_code)

    # Optional: Save to file
    save = input("\n📝 Save to file? (y/n): ").strip().lower()
    if save == "y":
        file_name = input("📁 Enter filename (e.g., generated_script.py): ").strip()
        try:
            with open(file_name, "w", encoding="utf-8") as f:
                f.write(generated_code)
            print(f"✅ Code saved to {file_name}")
        except Exception as e:
            print(f"❌ Error saving file: {e}")



import os
import pathlib
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))

from dotenv import load_dotenv

# Load .env variables
load_dotenv()

# Import from utils
from src.utils.file_loader import load_code
from src.core.llm_adapter import query_llm


# 🧪 Prompt template
TEST_SYSTEM_PROMPT = """You are a senior software testing engineer. Generate unit tests in Python for the following code. 
Use `pytest` or `unittest`. Return only valid code inside triple backticks. No explanations.
"""

# Generate tests from local code file
def generate_tests(file_path: str) -> str:
    if not os.path.exists(file_path):
        return f"❌ File not found: {file_path}"

    try:
        code = load_code(file_path)
        if code.startswith("❌"):
            return code

        prompt = f"{TEST_SYSTEM_PROMPT}\n\n```python\n{code}\n```"
        result = query_llm(prompt)

        if not result:
            return "❌ No test output returned."

        return result.encode("utf-8").decode("utf-8")
    except Exception as e:
        return f"❌ Error generating tests: {e}"

# Write tests to file and optionally run them (manual CLI)
def run_tests(test_code: str) -> str:
    import subprocess
    test_file = "temp_test_file.py"
    with open(test_file, "w", encoding="utf-8") as f:
        f.write(test_code)

    result = subprocess.run(["pytest", test_file], capture_output=True, text=True)
    os.remove(test_file)
    return result.stdout

# ✅ MAIN FUNCTION USED BY FastAPI

def generate_tests_for(idea: str) -> str:
    # Convert idea to path: "AI assistant" -> "./generated/ai_assistant/main.py"
    safe_path = idea.strip().lower().replace(" ", "_")
    file_path = f"./generated/{safe_path}/main.py"

    if not os.path.exists(file_path):
        return f"❌ Code not found: {file_path}"

    return generate_tests(file_path)

# ✅ For direct CLI testing
if __name__ == "__main__":
    print("🧪 Test Agent Started")
    path = input("📂 Enter Python file to generate tests for: ").strip()
    test_code = generate_tests(path)

    if test_code.startswith("❌"):
        print(test_code)
    else:
        output_path = f"tests/test_{pathlib.Path(path).stem}.py"
        os.makedirs("tests", exist_ok=True)
        with open(output_path, "w", encoding="utf-8") as f:
            f.write(test_code)
        print(f"✅ Tests written to {output_path}")
        print("🔎 Executing tests...\n")
        print(run_tests(test_code))



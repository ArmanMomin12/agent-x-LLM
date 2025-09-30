# src/agents/security_agent.py

import os
import sys

# Allow root-level imports
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))

from dotenv import load_dotenv
from src.core.llm_adapter import query_llm

load_dotenv()

SECURITY_SCAN_PROMPT = """
You are a senior security analyst.

Please analyze the following Python code for potential security issues. Look for:
- Unsafe input handling
- Use of insecure libraries
- Hardcoded secrets
- Insecure configurations
- Anything that violates security best practices

Respond in this format:
1. 🚨 Issues Found:
- Issue 1: Description
- Issue 2: Description

2. ✅ Suggestions:
- Fix 1: Description
- Fix 2: Description
"""

def run_security_scan(code: str) -> str:
    print("🔐 Running security scan...")
    if not code.strip():
        return "❌ No code provided for security analysis."
    prompt = SECURITY_SCAN_PROMPT + f"\n\n```python\n{code}\n```"
    response = query_llm(prompt)
    print("✅ Security scan completed.")
    return response

# Optional CLI test
if __name__ == "__main__":
    print("🔍 Security Agent Started")
    path = input("📂 Enter Python file to scan: ").strip()
    if not os.path.exists(path):
        print("❌ File not found.")
    else:
        with open(path, "r", encoding="utf-8") as f:
            code = f.read()
        report = run_security_scan(code)
        print("\n📋 Security Report:\n")
        print(report)



# src/core/prompt_engine.py

import textwrap

class PromptEngine:
    def __init__(self):
        pass

    def build_planner_prompt(self, user_goal: str) -> str:
        return textwrap.dedent(f"""
            You are a professional AI software architect.

            Your job is to create a detailed project plan for the following goal:

            🧠 GOAL:
            {user_goal}

            ✅ Break it down into sections:
            - Project Overview
            - Components (Frontend, Backend, Models, Tools, etc.)
            - Technology Stack
            - Roadmap (Phases)
            - Timeline (Weeks or Milestones)
            - Team & Skills Needed
            - Estimated Budget

            Respond in clean Markdown format.
        """)

    def build_code_writer_prompt(self, plan: dict, task_description: str = "") -> str:
        plan_summary = "\n".join([f"- **{k}**: {v}" for k, v in plan.items()])
        return textwrap.dedent(f"""
            You are a senior software engineer.

            Given this project plan:

            {plan_summary}

            Write Python code for this task:
            🧪 {task_description}

            Make sure the code:
            - Is well-commented
            - Follows best practices
            - Runs independently.
        """)

    def build_debugger_prompt(self, buggy_code: str, error_msg: str) -> str:
        return textwrap.dedent(f"""
            You are an expert Python debugger.

            Here is the code:
            ```python
            {buggy_code}
            ```

            And the error or issue:
            ```
            {error_msg}
            ```

            ✅ Identify the root cause and provide:
            - Explanation of the bug
            - Fixed version of the code.
        """)

    def build_tester_prompt(self, code_snippet: str) -> str:
        return textwrap.dedent(f"""
            You are a software testing expert.

            Write unit tests in Python for the following code:
            ```python
            {code_snippet}
            ```

            ✅ Use unittest or pytest and cover all edge cases.
        """)



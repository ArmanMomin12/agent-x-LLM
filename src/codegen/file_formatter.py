import re
import textwrap

def clean_code_output(code: str) -> str:
    """
    Cleans up raw code returned by the LLM.
    - Strips markdown backticks if present
    - Removes leading/trailing whitespace
    - Dedents the code properly
    """
    # Remove Markdown-style code blocks
    code = re.sub(r"^```(python)?", "", code.strip(), flags=re.MULTILINE)
    code = re.sub(r"```$", "", code.strip(), flags=re.MULTILINE)

    # Dedent and strip excess blank lines
    code = textwrap.dedent(code).strip()
    return code

def extract_code_blocks(text: str) -> list:
    """
    Extracts all code blocks from an LLM response using markdown triple backticks.
    Returns a list of cleaned code strings.
    """
    code_blocks = re.findall(r"```(?:python)?\n(.*?)```", text, re.DOTALL)
    return [clean_code_output(block) for block in code_blocks]

def wrap_as_code_block(code: str, lang: str = "python") -> str:
    """
    Wraps the given code in triple backticks with optional language tag.
    """
    return f"```{lang}\n{code.strip()}\n```"

def truncate_code(code: str, max_lines: int = 50) -> str:
    """
    Truncates code output for logging or previews, adding '...'.
    """
    lines = code.strip().split("\n")
    if len(lines) > max_lines:
        return "\n".join(lines[:max_lines]) + "\n..."
    return code




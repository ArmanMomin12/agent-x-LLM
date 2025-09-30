import ast

def is_syntax_valid(code: str) -> bool:
    """
    Returns True if code is syntactically valid Python, else False.
    """
    try:
        ast.parse(code)
        return True
    except SyntaxError:
        return False

def get_syntax_errors(code: str) -> str:
    """
    Returns detailed syntax error info if code is invalid.
    """
    try:
        ast.parse(code)
        return "✅ No syntax errors found."
    except SyntaxError as e:
        return f"❌ Syntax Error on line {e.lineno}, col {e.offset}: {e.msg}"

def assert_syntax(code: str):
    """
    Raises a SyntaxError if the code is invalid (for use in pipelines).
    """
    ast.parse(code)




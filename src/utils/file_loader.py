import os

def load_code(path: str) -> str:
    """
    Loads Python code from the given file path.
    Returns the code as a string.
    """
    if not os.path.exists(path):
        raise FileNotFoundError(f"❌ File not found: {path}")

    with open(path, "r", encoding="utf-8") as file:
        return file.read()



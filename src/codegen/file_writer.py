import os

def ensure_directory_exists(file_path: str):
    """
    Ensures the directory for the given file path exists.
    If it doesn't, it creates the necessary folders.
    """
    dir_name = os.path.dirname(file_path)
    if dir_name and not os.path.exists(dir_name):
        os.makedirs(dir_name)
        print(f"📁 Created directory: {dir_name}")

def write_code_to_file(file_path: str, code: str, mode: str = "w"):
    """
    Writes code to the specified file.
    mode: "w" = overwrite, "a" = append
    """
    ensure_directory_exists(file_path)
    try:
        with open(file_path, mode, encoding="utf-8") as f:
            f.write(code)
        print(f"✅ Code written to: {file_path}")
    except Exception as e:
        print(f"❌ Error writing to file: {e}")

def read_file(file_path: str) -> str:
    """
    Reads content from the given file and returns it as a string.
    """
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            return f.read()
    except FileNotFoundError:
        print(f"⚠️ File not found: {file_path}")
        return ""





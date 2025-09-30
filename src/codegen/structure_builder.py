import os

IGNORE_FOLDERS = {'.git', '__pycache__', '.idea', '.vscode', 'venv', 'env', '.mypy_cache', '.pytest_cache', '.DS_Store'}
IGNORE_FILES = {'.DS_Store'}

def build_structure(root_dir: str, include_preview=False, max_preview_lines=5) -> dict:
    """
    Recursively builds the file structure starting from root_dir.
    Optionally includes file content previews.
    Returns a nested dictionary representation.
    """
    structure = {}

    for root, dirs, files in os.walk(root_dir):
        # Skip ignored folders
        dirs[:] = [d for d in dirs if d not in IGNORE_FOLDERS]

        rel_path = os.path.relpath(root, root_dir)
        current = structure
        if rel_path != '.':
            for part in rel_path.split(os.sep):
                current = current.setdefault(part, {})

        for file in files:
            if file in IGNORE_FILES:
                continue
            if include_preview:
                file_path = os.path.join(root, file)
                preview = read_file_preview(file_path, max_preview_lines)
                current[file] = {"preview": preview}
            else:
                current[file] = "file"

    return structure

def read_file_preview(file_path, max_lines=5):
    """
    Returns the first few lines of a file for preview.
    """
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            return ''.join(f.readlines()[:max_lines]).strip()
    except Exception as e:
        return f"[Error reading file: {e}]"

def print_structure(structure, indent=0):
    """
    Pretty-prints the structure dictionary as a tree view.
    """
    for name, content in structure.items():
        if isinstance(content, dict):
            print('  ' * indent + f"📁 {name}/")
            print_structure(content, indent + 1)
        else:
            print('  ' * indent + f"📄 {name}")




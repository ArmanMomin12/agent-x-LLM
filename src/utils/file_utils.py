# src/utils/file_util.py

import os
import json
from datetime import datetime

def save_to_file(file_path: str, content: str) -> bool:
    """Saves string content to a file."""
    try:
        os.makedirs(os.path.dirname(file_path), exist_ok=True)
        with open(file_path, "w", encoding="utf-8") as f:
            f.write(content)
        print(f"✅ File saved at: {file_path}")
        return True
    except Exception as e:
        print(f"❌ Error saving file: {e}")
        return False


def read_from_file(file_path: str) -> str:
    """Reads string content from a file."""
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            return f.read()
    except FileNotFoundError:
        print(f"⚠️ File not found: {file_path}")
        return ""
    except Exception as e:
        print(f"❌ Error reading file: {e}")
        return ""


def append_to_file(file_path: str, content: str) -> bool:
    """Appends string content to a file."""
    try:
        with open(file_path, "a", encoding="utf-8") as f:
            f.write(content + "\n")
        return True
    except Exception as e:
        print(f"❌ Error appending to file: {e}")
        return False


def save_json(file_path: str, data: dict) -> bool:
    """Saves dictionary data to a JSON file."""
    try:
        os.makedirs(os.path.dirname(file_path), exist_ok=True)
        with open(file_path, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=4)
        print(f"✅ JSON saved at: {file_path}")
        return True
    except Exception as e:
        print(f"❌ Error saving JSON: {e}")
        return False


def load_json(file_path: str) -> dict:
    """Loads data from a JSON file."""
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            return json.load(f)
    except FileNotFoundError:
        print(f"⚠️ JSON file not found: {file_path}")
        return {}
    except Exception as e:
        print(f"❌ Error loading JSON: {e}")
        return {}


def get_timestamped_filename(prefix: str, ext: str = "txt", folder: str = "outputs") -> str:
    """Generates a filename with timestamp (e.g., outputs/code_2025-07-03_10-30.txt)"""
    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    filename = f"{prefix}_{timestamp}.{ext}"
    os.makedirs(folder, exist_ok=True)
    return os.path.join(folder, filename)



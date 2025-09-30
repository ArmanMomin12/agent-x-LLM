import os
import base64
import requests
from dotenv import load_dotenv

# ✅ Load GitHub token from .env
load_dotenv()
GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")
GITHUB_USERNAME = os.getenv("GITHUB_USERNAME")
REPO_NAME = os.getenv("GITHUB_REPO_NAME")

def upload_to_github(file_path: str, repo_path: str, commit_message: str = "Add file via uploader") -> bool:
    """
    Uploads a file to a GitHub repository using the REST API.

    Args:
        file_path (str): Local file path to upload.
        repo_path (str): Target path in the GitHub repo.
        commit_message (str): Commit message.

    Returns:
        bool: True if upload succeeded, False otherwise.
    """
    if not all([GITHUB_TOKEN, GITHUB_USERNAME, REPO_NAME]):
        print("❌ Missing GitHub credentials in .env.")
        return False

    # Read file and encode it to Base64
    try:
        with open(file_path, "rb") as f:
            content = base64.b64encode(f.read()).decode("utf-8")
    except Exception as e:
        print(f"❌ Error reading file: {e}")
        return False

    url = f"https://api.github.com/repos/{GITHUB_USERNAME}/{REPO_NAME}/contents/{repo_path}"

    headers = {
        "Authorization": f"token {GITHUB_TOKEN}",
        "Accept": "application/vnd.github.v3+json"
    }

    # Check if file already exists to include sha
    get_response = requests.get(url, headers=headers)
    sha = get_response.json().get("sha") if get_response.status_code == 200 else None

    payload = {
        "message": commit_message,
        "content": content,
        "branch": "main"
    }
    if sha:
        payload["sha"] = sha

    response = requests.put(url, headers=headers, json=payload)

    if response.status_code in [200, 201]:
        print(f"✅ Uploaded to GitHub: {repo_path}")
        return True
    else:
        print(f"❌ GitHub upload failed: {response.status_code}\n{response.text}")
        return False

# ✅ Example usage
if __name__ == "__main__":
    # Customize these
    local_file = "outputs/context_snapshot_2025-07-03_11-28-42.json"
    target_repo_path = "logs/context_snapshot.json"
    commit_msg = "Upload context snapshot"
    
    upload_to_github(local_file, target_repo_path, commit_msg)



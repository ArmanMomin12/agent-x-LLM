import os
import subprocess
import sys

def install_packages(requirements_file="requirements.txt"):
    if os.path.exists(requirements_file):
        print(f"📦 Installing dependencies from {requirements_file}...")
        subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", requirements_file])
    else:
        print(f"❌ No {requirements_file} found!")

def install_dev_dependencies(dev_file="requirements-dev.txt"):
    if os.path.exists(dev_file):
        print(f"📦 Installing dev dependencies from {dev_file}...")
        subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", dev_file])
    else:
        print("ℹ️ No dev dependencies file found. Skipping.")

def install_submodules():
    print("🔁 Updating Git submodules (if any)...")
    subprocess.call(["git", "submodule", "update", "--init", "--recursive"])

def install_local_packages():
    local_dirs = ["./src/", "./libs/"]
    for directory in local_dirs:
        if os.path.isdir(directory):
            has_setup = os.path.exists(os.path.join(directory, "setup.py"))
            has_pyproject = os.path.exists(os.path.join(directory, "pyproject.toml"))
            if has_setup or has_pyproject:
                print(f"📂 Installing local package from {directory}...")
                subprocess.call([sys.executable, "-m", "pip", "install", "-e", directory])
            else:
                print(f"⚠️ Skipping {directory}: no setup.py or pyproject.toml found.")

def download_models():
    print("🧠 Downloading required models (optional step)...")
    try:
        from sentence_transformers import SentenceTransformer
        SentenceTransformer('all-MiniLM-L6-v2')
        print("✅ Model downloaded.")
    except ImportError:
        print("⚠️ SentenceTransformers not installed. Skipping model download.")

def main():
    install_submodules()
    install_packages()
    install_dev_dependencies()
    install_local_packages()
    download_models()
    print("✅ All dependencies installed successfully!")

if __name__ == "__main__":
    main()



import os
import re
from agents.planner_agent import generate_plan

def get_folder_name(user_input: str) -> str:
    """Convert project name into safe folder name."""
    name = user_input.lower().strip()
    name = re.sub(r"[^a-z0-9]+", "_", name)  # replace non-alphanumerics with "_"
    name = re.sub(r"_+", "_", name)           # collapse multiple "_"
    return name.strip("_")

def ensure_main_py(folder: str):
    os.makedirs(folder, exist_ok=True)
    main_file = os.path.join(folder, "main.py")
    if not os.path.exists(main_file):
        with open(main_file, "w") as f:
            f.write("# Auto-generated main.py\n")
            f.write("print('Hello from AutoCode-GPT-X!')\n")
    return main_file

if __name__ == "__main__":
    user_input = input("Enter your project idea: ")

    # Step 1: sanitize folder name
    folder_name = get_folder_name(user_input)
    output_dir = os.path.join("generated", folder_name)

    # Step 2: create folder & main.py
    main_file = ensure_main_py(output_dir)

    # Step 3: generate project plan
    plan = generate_plan(user_input)

    if plan:
        print("\nProject Plan:")
        for part, task in plan.items():
            print(f"- {part}: {task}")

        print(f"\n✅ main.py created at {main_file}")
    else:
        print("No plan generated. Please try again.")

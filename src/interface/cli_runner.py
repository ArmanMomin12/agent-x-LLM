# src/interface/clirunner.py

import os
import sys
from dotenv import load_dotenv

# Setup import paths
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))

from src.agents.planner_agent import generate_plan
from src.agents.writer_agent import write_code
from src.agents.test_agent import generate_tests
from src.agents.doc_agent import generate_readme_and_gitignore
from src.agents.docker_agent import generate_dockerfile

load_dotenv()

def menu():
    print("\nAutoCode-GPT-X CLI Runner")
    print("----------------------------")
    print("1 Generate Project Plan")
    print("2 Generate Code")
    print("3 Generate Tests")
    print("4 Generate README & .gitignore")
    print("5 Generate Dockerfile")
    print("0 Exit")

def run():
    while True:
        menu()
        choice = input("Choose an option: ").strip()

        if choice == "0":
            print("Exiting...")
            break

        idea = input("Enter your project idea: ").strip()

        if choice == "1":
            print("\nGenerating Plan...")
            plan = generate_plan(idea)
            print(plan)

        elif choice == "2":
            print("\nGenerating Code...")
            code = write_code(idea)
            print(code)

        elif choice == "3":
            print("\nGenerating Tests...")
            tests = generate_tests(idea)
            print(tests)

        elif choice == "4":
            print("\nGenerating README and .gitignore...")
            docs = generate_readme_and_gitignore(idea)
            print("README.md:\n", docs.get("README.md", "No README generated."))
            print("\n.gitignore:\n", docs.get(".gitignore", "No .gitignore generated."))

        elif choice == "5":
            print("\nGenerating Dockerfile...")
            dockerfile = generate_dockerfile(idea)
            print(dockerfile)

        else:
            print("Invalid option. Please try again.")

if __name__ == "__main__":
    run()

# src/interface/cli_runner.py

import os
import sys

# Add project root to sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))

from src.agents.planner_agent import generate_plan
from src.agents.code_writer_agent import run_code_writer
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../src")))
from src.core.memory_manager import MemoryManager
from src.core.context_tracker import ContextTracker

def main():
    print("🤖 Welcome to AutoCode-GPT-X CLI Interface\n")

    # Setup
    memory_manager = MemoryManager()
    context_tracker = memory_manager.load_context()  # Try to load if saved

    while True:
        print("\nChoose an option:")
        print("1. Generate Plan")
        print("2. Run Code Writer")
        print("3. View Context Summary")
        print("4. Save Context")
        print("5. Load Context")
        print("6. Exit")

        choice = input("Enter your choice (1-6): ").strip()

        if choice == "1":
            project_idea = input("\nEnter your project idea: ").strip()
            print("\n🧠 Generating plan...")
            try:
                context_tracker.set_goal(project_idea)
                plan = generate_plan(project_idea, memory_manager, context_tracker)
                print("\n✅ Generated Plan:\n")
                print(plan)
            except Exception as e:
                print(f"❌ Error generating plan: {e}")

        elif choice == "2":
            try:
                print("\n⚙️ Running Code Writer Agent...")
                result = run_code_writer(memory_manager, context_tracker)
                print("\n✅ Code Writer Result:\n")
                print(result)
            except Exception as e:
                print(f"❌ Error running code writer: {e}")

        elif choice == "3":
            print("\n📚 Full Context:")
            print(context_tracker.get_context())

        elif choice == "4":
            memory_manager.save_context(context_tracker)

        elif choice == "5":
            context_tracker = memory_manager.load_context()

        elif choice == "6":
            print("👋 Exiting. Goodbye!")
            break

        else:
            print("⚠️ Invalid choice. Please try again.")

if __name__ == "__main__":
    main()



import os
import sys
import time
from dotenv import load_dotenv

# ✅ Setup project root for imports
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))

# ✅ Load environment variables
load_dotenv()

# Core Modules
from src.core.context_tracker import ContextTracker
from src.core.memory_manager import MemoryManager
from src.utils.time_utils import Timer, get_current_timestamp
from src.utils.cost_estimator import estimate_cost
from src.utils.file_utils import save_json, get_timestamped_filename

# AI Agents
from src.agents.planner_agent import generate_plan
from src.agents.code_writer_agent import run_code_writer
from src.agents.self_debugger_agent import debug_code
from src.agents.doc_agent import generate_docs
from src.agents.docker_agent import generate_dockerfile

from src.agents.test_agent import run_tests

from src.agents.security_agent import run_security_scan  # ✅ Add this file if not exists
from src.agents.performance_agent import run_performance_tests  # ✅ Add this file if not exists

# Vector Store
from src.vector_store.weaviate_adapter import store_context_vector

# ✅ Initialize context and memory
context = ContextTracker()
memory = MemoryManager()


def log_stage_event(stage, detail):
    print(f"🔹 [{stage}] →", detail)


def validate_plan_structure(plan):
    return isinstance(plan, dict) and "tasks" in plan


def orchestrate_project(user_prompt: str, session_id="latest"):
    print(f"\n🔁 Orchestration started at {get_current_timestamp()}...")

    # 1. 📌 Planning
    with Timer("📌 Planning phase"):
        plan = generate_plan(user_prompt)
        if not plan or not validate_plan_structure(plan):
            print("❌ Planning failed. Invalid plan structure.")
            return
        context.log_event("Planning completed", "Structured plan received.")
        log_stage_event("Planning", plan)

    # 2. 💰 Estimating cost
    with Timer("🧾 Estimating cost"):
        cost = estimate_cost(plan)
        context.update_variable("project_cost_estimate", cost)
        print(f"💰 Estimated Cost: ${cost['estimated_total_cost_usd']} | Team Size: {cost['estimated_team_size']} | Duration: {cost['estimated_duration_weeks']} weeks")
        log_stage_event("Cost Estimate", cost)

    # 3. 💻 Code Generation
    with Timer("💻 Code generation"):
        generated_code = run_code_writer(plan)
        context.log_event("Code generation completed", "Initial code generated.")
        log_stage_event("Code Generated", generated_code)

    # 4. 🧠 Debugging
    with Timer("🧠 Debugging"):
        debugged_code = debug_code(generated_code)
        context.log_event("Debugging completed", "Bugs fixed and logic verified.")

    # 5. ✅ Testing
    with Timer("✅ Unit Testing"):
        test_results = run_tests(debugged_code)
        context.log_event("Unit Testing completed", f"Results: {test_results}")

    # 6. 🔁 Integration Testing
    with Timer("🔁 Integration Testing"):
        integration_results = run_integration_tests(debugged_code)
        context.log_event("Integration Tests completed", f"Integration Results: {integration_results}")

    # 7. 🔐 Security Scan
    with Timer("🔐 Security Scan"):
        security_report = run_security_scan(debugged_code)
        context.log_event("Security Scan completed", "Security issues analyzed.")

    # 8. 🚀 Performance Testing
    with Timer("🚀 Performance Testing"):
        perf_report = run_performance_tests(debugged_code)
        context.log_event("Performance Tests completed", "Performance validated.")

    # 9. 📄 Documentation
    with Timer("📄 Documentation"):
        documentation = generate_docs(debugged_code)
        context.log_event("Documentation generated", "README, API docs created.")

    # 10. 🐳 Docker
    with Timer("🐳 Dockerization"):
        dockerfile = generate_dockerfile(debugged_code)
        context.log_event("Dockerfile created", "Docker setup complete.")

    # 11. 🐙 GitHub
    with Timer("🐙 GitHub Upload"):
        repo_url = push_to_github(debugged_code, documentation, dockerfile)
        context.update_variable("github_repo", repo_url)
        context.log_event("GitHub Push completed", repo_url)

    # 12. 🧠 Vector Store
    with Timer("🧠 Vector Storage"):
        store_context_vector(context.get_context())

    # 🔒 Save context
    memory.save_context(context, session_id=session_id)
    snapshot = context.get_context()
    snapshot_file = get_timestamped_filename("context_snapshot", "json", folder="outputs")
    save_json(snapshot_file, snapshot)

    # ✅ Final Output
    print("\n🎉 Project orchestration complete!")
    print("\n🧠 Final Context Snapshot:", snapshot)
    print("\n💻 Final Generated Code:\n", debugged_code)
    print("\n📄 Documentation:\n", documentation)
    print("\n🐙 GitHub Repo:\n", repo_url)


if __name__ == "__main__":
    default_prompt = "Create a full-stack AI assistant that generates, tests, documents, and deploys code."
    orchestrate_project(default_prompt, session_id="ai_assistant")



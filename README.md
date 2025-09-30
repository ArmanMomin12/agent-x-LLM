Agent-X 🤖🚀

A beginner-friendly AutoGPT-style AI agent project.
This system demonstrates AI agent capabilities, automates tasks, and provides a structured backend with optional frontend integration.

🛠 Features

LLM Model Integration: Uses Groq-compatible language models for reasoning and code generation.

Test Agent: Automatically runs unit tests, validates code, and provides feedback.

Task Planner Agent: Plans multi-step coding tasks using AI reasoning.

Self-Debugger Agent: Detects and fixes bugs in generated code.

Streamlit UI: Interactive interface for running agents, viewing logs, and generating outputs.

Activity Tracking: Monitors agent actions, decisions, and outputs in real-time.

Docker Support: Run the system inside a container for portability.

Extensible Architecture: Add new agents or features easily.

🛠 Tech Stack

Backend: Python 3.10, Flask

Frontend/UI: Streamlit

LLM Integration: Groq-compatible models

Database: PostgreSQL (optional, for activity logs)

Testing: Pytest / Unit tests

Docker: Containerized deployment

Data & Visualization: CSV, logs, JSON outputs

Project Structure
Agent-X/
├── Dockerfile
├── pyproject.toml
├── requirements.txt
├── main.py
├── LICENSE
├── README.md
├── .gitignore
├── .env.example
├── src/
│   ├── agents/           # Planner, Test, Self-Debugger, Task agents
│   ├── interface/        # Streamlit UI files
│   ├── utils/            # Helper functions, logging
│   └── models/           # Model configs, tokenizers, LLM wrappers
├── logs/                 # Activity and agent logs
└── generated/            # Generated code outputs


Run the Streamlit UI
streamlit run src/interface/streamlit_ui.py


(Optional) Run with Docker
docker build -t agent-x .
docker run -p 8501:8501 agent-x

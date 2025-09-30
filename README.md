# 🚀 Agent X 🤖🛠️
**AI Software Engineer Assistant** – Created by **Arman Momin**  
*Fresher / Beginner Level Project*

---

## 🌟 Overview
Agent X is a **multi-agent AI system** that automates software engineering tasks.  
It uses **Groq LLM models**, a **Streamlit interface**, and multiple agents for **code generation, testing, and debugging**.  

> Designed for **learning, experimentation, and demonstration** of AI engineering pipelines.

---

## ✨ Features
- 🧠 **Groq LLM Integration** – AI reasoning & code generation  
- ✅ **Test Agent** – Runs unit tests and validates code  
- 📝 **Task Planner Agent** – Plans multi-step tasks intelligently  
- 🐞 **Self-Debugger Agent** – Fixes bugs automatically  
- 💻 **Streamlit UI** – Interactive interface for agents & outputs  
- 📊 **Activity Tracking** – Logs agent actions and decisions  
- 🐳 **Docker Support** – Easy containerized deployment  
- 🔧 **Extensible Architecture** – Add new agents or features easily  

---

## ⚡ Tech Stack
| Layer | Tools / Libraries |
|-------|-----------------|
| Backend | Python 3.10, Flask |
| Frontend / UI | Streamlit |
| AI | Groq-compatible LLM |
| Testing | Pytest |
| Utilities | Python-dotenv, tqdm |
| Deployment | Docker |

---

## 🛠 Installation & Setup

### 1️⃣ Clone the repo
```bash
git clone https://github.com/ArmanMomin12/agent-x-LLM.git
cd agent-x-LLM
2️⃣ Create virtual environment

    python -m venv venv
    # Activate venv:
    source venv/bin/activate      # Linux / Mac
    venv\Scripts\activate         # Windows
3️⃣  Run the Streamlit UI
    streamlit run src/interface/streamlit_ui.py

📁 Project Structure

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
│   ├── agents/
│   ├── interface/
│   ├── utils/
│   └── models/
├── logs/
└── generated/





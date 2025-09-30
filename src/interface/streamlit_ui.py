# src/interface/streamlit_ui.py

import os
import sys
import requests
import streamlit as st
from dotenv import load_dotenv

# 🧪 Path setup
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))

# Load env
load_dotenv()

# Backend URL
BACKEND_URL = "http://localhost:8000"
GENERATED_DIR = "generated"

# ------------------------- 🌌 Page Config -------------------------
st.set_page_config(
    page_title="⚡ AutoCode-GPT-X",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ------------------------- 🎨 Custom CSS -------------------------
st.markdown("""
<style>
    body, html {
        height: 100%;
        margin: 0;
        display: flex;
        flex-direction: column;
        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
    }

    main {
        flex: 1;
    }

    /* Header (kept as-is) */
    .header {
        background: linear-gradient(90deg, #141e30, #243b55);
        padding: 1rem 2rem;
        border-radius: 12px;
        margin-bottom: 20px;
        color: white;
        position: relative;
        top: -60px;
        left: -75px;
        width: 2500px;
        z-index: 1000;
    }
    .header h1 {
        margin: 0;
        font-size: 2rem;
        color: #00e5ff;
    }
    .nav-links {
        margin-top: 10px;
    }
    .nav-links a {
        margin-right: 20px;
        text-decoration: none;
        color: #00e5ff;
        font-weight: bold;
    }

    /* Cards */
    .card {
        background: #1e293b;
        border-radius: 15px;
        padding: 20px;
        margin: 20px 0;
        color: white;
        box-shadow: 0 4px 15px rgba(0,0,0,0.5);
    }

    /* Buttons */
    .stButton>button {
        background: linear-gradient(90deg, #00c6ff, #0072ff);
        color: white;
        border-radius: 10px;
        padding: 10px 25px;
        font-weight: bold;
        border: none;
        transition: 0.3s;
        margin-top: 10px;
    }
    .stButton>button:hover {
        transform: scale(1.05);
    }

    /* Footer (kept as-is) */
    .footer {
        background: #111;
        color: #e0e0e0;
        padding: 15px 10px;
        display: flex;
        flex-direction: column;
        align-items: center;
        gap: 10px;
        border-top: 1px solid #333;
        position: relative;
        top: 720px;
        left: -75px;
        width: 100%;
        z-index: 1000;
    }
    .social-links {
        display: flex;
        gap: 20px;
    }
    .social-links a img {
        width: 30px;
        height: 30px;
        transition: transform 0.2s;
    }
    .social-links a img:hover {
        transform: scale(1.2);
    }
    #copy {
        font-size: 0.9rem;
        color: #aaa;
    }

    /* Space main content to avoid overlap */
    .stApp > main {
        padding-top: 120px;    /* space for header */
        padding-bottom: 100px; /* space for footer */
    }

    /* Limit content width and center */
    .stApp main .block-container {
        max-width: 1200px;
        margin: auto;
    }
</style>
""", unsafe_allow_html=True)

# ------------------------- 🚀 Header -------------------------
st.markdown("""
<div class="header">
    <h1>🤖 AutoCode-GPT-X</h1>
    <div class="nav-links">
        <a href="#">🏠 Home</a>
        <a href="#">⚡ Features</a>
        <a href="#">📘 Docs</a>
        <a href="#">📞 Contact</a>
    </div>
</div>
""", unsafe_allow_html=True)

# ------------------------- 📝 Sidebar -------------------------
with st.sidebar:
    st.header("⚙️ Controls")
    idea = st.text_area("💡 Project Idea", "Build an AI assistant", height=100)
    project_type = st.selectbox("📌 Project Type", ["Web App", "AI Agent", "Data Science", "Automation", "Other"])
    custom_prompt = st.text_area("✍️ Custom Instructions", "Focus on scalability and modular design.")
    temperature = st.slider("🎯 Creativity", 0.0, 1.0, 0.3)
    model = st.selectbox("🧠 Model", ["llama-3.1-8b-instant", "gpt-4", "mistral-7b"])
    run_button = st.button("🚀 Launch Agent")

payload = {"idea": idea, "project_type": project_type, "instructions": custom_prompt, "temperature": temperature, "model": model}

# ------------------------- ⚡ Main Panel -------------------------
if run_button:
    if not idea.strip():
        st.warning("⚠️ Please enter a valid project idea.")
    else:
        with st.spinner("🤔 Agent is generating your project..."):
            results = {}
            endpoints = ["plan", "write", "test", "docs", "docker"]
            for endpoint in endpoints:
                try:
                    res = requests.post(f"{BACKEND_URL}/{endpoint}/", json=payload)
                    res.raise_for_status()
                    results[endpoint] = res.json()
                except Exception as e:
                    results[endpoint] = {"success": False, "error": str(e)}

        st.success("✅ Project Generated Successfully!")

        # Tabs
        tabs = st.tabs(["🧭 Plan", "🧾 Code", "🧪 Tests", "📄 Docs", "🐳 Docker", "📦 Raw JSON"])

        # --- Project Plan ---
        with tabs[0]:
            st.subheader("🧭 Project Plan")
            plan_result = results.get("plan", {})
            plan_text = ""
            if isinstance(plan_result, dict):
                if "plan" in plan_result and isinstance(plan_result["plan"], dict):
                    plan_text = "\n".join(f"{k}: {v}" for k, v in plan_result["plan"].items())
                else:
                    plan_text = plan_result.get("plan") or plan_result.get("tasks") or ""
            elif isinstance(plan_result, list):
                plan_text = "\n".join(str(item) for item in plan_result)
            else:
                plan_text = str(plan_result)
            if not plan_text.strip():
                st.warning("❌ Failed to generate plan.")
            else:
                st.markdown("### 🚀 Roadmap")
                for idx, line in enumerate(plan_text.split("\n")):
                    if line.strip():
                        st.markdown(f"**Step {idx+1}:** {line.strip()}")

        # --- Code ---
        with tabs[1]:
            st.subheader("🧾 Generated Code (main.py)")
            code_text = results.get("write", {}).get("code") or "# ❌ No code returned"
            st.markdown(f"<div class='card'><pre>{code_text}</pre></div>", unsafe_allow_html=True)

        # --- Tests ---
        with tabs[2]:
            st.subheader("🧪 Unit Tests")
            test_text = results.get("test", {}).get("tests") or "# ❌ No tests returned"
            st.markdown(f"<div class='card'><pre>{test_text}</pre></div>", unsafe_allow_html=True)

        # --- Docs ---
        with tabs[3]:
            st.subheader("📄 Documentation")
            docs_text = results.get("docs", {}).get("docs") or "❌ No documentation returned."
            st.markdown(f"<div class='card'><pre>{docs_text}</pre></div>", unsafe_allow_html=True)

        # --- Docker ---
        with tabs[4]:
            st.subheader("🐳 Dockerfile")
            docker_text = results.get("docker", {}).get("docker") or "❌ No Dockerfile returned."
            st.markdown(f"<div class='card'><pre>{docker_text}</pre></div>", unsafe_allow_html=True)

        # --- Raw JSON ---
        with tabs[5]:
            st.json(results)

# ------------------------- 🔻 Footer -------------------------
st.markdown("""
<footer class="footer">
    <!-- Social links -->
    <div class="social-links">
        <a href="https://www.linkedin.com/in/yourprofile" target="_blank">
            <img src="https://cdn-icons-png.flaticon.com/512/174/174857.png" alt="LinkedIn" />
        </a>
        <a href="https://github.com/yourusername" target="_blank">
            <img src="https://cdn-icons-png.flaticon.com/512/25/25231.png" alt="GitHub" />
        </a>
        <a href="https://twitter.com/yourusername" target="_blank">
            <img src="https://cdn-icons-png.flaticon.com/512/733/733579.png" alt="Twitter" />
        </a>
    </div>
    <span id="copy">© 2025 AutoCode-GPT-X</span>
</footer>
""", unsafe_allow_html=True)

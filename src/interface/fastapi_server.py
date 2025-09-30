# src/interface/fastapi_server.py

import os
import sys
import logging
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional

# Set project root for imports
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))

# Import custom AI agents
from src.agents.planner_agent import generate_plan
from src.agents.writer_agent import write_code
from src.agents.test_agent import generate_tests_for
from src.agents.doc_agent import generate_readme_and_gitignore
from src.agents.docker_agent import generate_dockerfile

# Initialize FastAPI app
app = FastAPI(
    title="⚙️ AutoCode-GPT-X API",
    description="An intelligent API that automates code planning, writing, testing, documentation, and Dockerization.",
    version="1.0.0"
)

# Allow CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Replace with frontend domain in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Input schema
class ProjectRequest(BaseModel):
    idea: str
    temperature: Optional[float] = 0.3
    model: Optional[str] = "llama-3.1-8b-instant"  # supported model

# Root endpoint
@app.get("/")
def root():
    return {"message": "✅ AutoCode-GPT-X backend is running!"}

# --- Helper function for fallback ---
def fallback_plan(idea: str):
    return {
        "goal": idea,
        "tasks": ["Define requirements", "Design architecture", "Implement modules", "Test and debug", "Deploy"]
    }

def fallback_code():
    return "# Auto-generated fallback code\nprint('Hello from AutoCode-GPT-X!')"

def fallback_tests():
    return "# Fallback unit tests\nprint('No tests generated.')"

def fallback_docs():
    return "# Fallback documentation\nNo docs generated."

def fallback_docker():
    return "# Fallback Dockerfile\nFROM python:3.9-slim"

# --- Plan endpoint ---
@app.post("/plan/")
def plan_code(req: ProjectRequest):
    if not req.idea.strip():
        raise HTTPException(status_code=400, detail="Prompt cannot be empty")
    try:
        plan = generate_plan(req.idea, temperature=req.temperature, model=req.model)
        return {"success": True, "plan": plan}
    except Exception as e:
        logging.exception("Planning failed")
        return {"success": False, "plan": fallback_plan(req.idea), "error": str(e)}

# --- Write code endpoint ---
@app.post("/write/")
def write_code_endpoint(req: ProjectRequest):
    if not req.idea.strip():
        raise HTTPException(status_code=400, detail="Prompt cannot be empty")
    try:
        code = write_code(req.idea)
        return {"success": True, "code": code}
    except Exception as e:
        logging.exception("Code generation failed")
        return {"success": False, "code": fallback_code(), "error": str(e)}

# --- Test generation endpoint ---
@app.post("/test/")
def generate_tests_endpoint(req: ProjectRequest):
    if not req.idea.strip():
        raise HTTPException(status_code=400, detail="Prompt cannot be empty")
    try:
        tests = generate_tests_for(req.idea)
        return {"success": True, "tests": tests}
    except Exception as e:
        logging.exception("Test generation failed")
        return {"success": False, "tests": fallback_tests(), "error": str(e)}

# --- Documentation endpoint ---
@app.post("/docs/")
def docs_endpoint(req: ProjectRequest):
    if not req.idea.strip():
        raise HTTPException(status_code=400, detail="Prompt cannot be empty")
    try:
        docs = generate_readme_and_gitignore(req.idea)
        return {"success": True, "docs": docs}
    except Exception as e:
        logging.exception("Documentation generation failed")
        return {"success": False, "docs": fallback_docs(), "error": str(e)}

# --- Dockerfile endpoint ---
@app.post("/docker/")
def dockerfile_endpoint(req: ProjectRequest):
    if not req.idea.strip():
        raise HTTPException(status_code=400, detail="Prompt cannot be empty")
    try:
        dockerfile = generate_dockerfile(req.idea)
        return {"success": True, "docker": dockerfile}
    except Exception as e:
        logging.exception("Dockerfile generation failed")
        return {"success": False, "docker": fallback_docker(), "error": str(e)}

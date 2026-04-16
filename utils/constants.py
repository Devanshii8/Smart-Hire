import os
from dotenv import load_dotenv

import streamlit as st

load_dotenv()

def get_secret_or_env(key, default=None):
    try:
        # Streamlit secrets usually acts as a dictionary
        if key in st.secrets:
            return st.secrets[key]
    except Exception:
        pass
    return os.getenv(key, default)

# Embedding config
EMBEDDING_MODEL_NAME = "sentence-transformers/all-MiniLM-L6-v2"
FAISS_INDEX_PATH = "data/faiss_index/smart_hire_index.faiss"

# Scoring weights
WEIGHT_SEMANTIC = 0.40
WEIGHT_SKILL = 0.20
WEIGHT_EXPERIENCE = 0.20
WEIGHT_PROJECT = 0.10
WEIGHT_EDUCATION = 0.10

# Matching thresholds
SHORTLIST_THRESHOLD = 0.65

# Email config
SMTP_HOST = get_secret_or_env("SMTP_HOST", "smtp.gmail.com")
SMTP_PORT = int(get_secret_or_env("SMTP_PORT", 587))
SMTP_EMAIL = get_secret_or_env("SMTP_EMAIL", "")
SMTP_PASSWORD = get_secret_or_env("SMTP_PASSWORD", "")
HR_COMPANY_NAME = get_secret_or_env("HR_COMPANY_NAME", "SmartHire AI Inc.")

# LLM Provider Configuration
LLM_PROVIDER = get_secret_or_env("LLM_PROVIDER", "gemini")

# LLM Model (Gemini 2.0 Flash recommended for cost/speed)
LLM_MODEL_NAME = get_secret_or_env("LLM_MODEL_NAME", "gemini-1.5-flash")

# Groq Model (Requires GROQ_API_KEY)
GROQ_MODEL_NAME = get_secret_or_env("GROQ_MODEL_NAME", "llama-3.3-70b-versatile")

# Ollama Model (Requires Ollama running locally)
OLLAMA_MODEL_NAME = get_secret_or_env("OLLAMA_MODEL_NAME", "llama3")
OLLAMA_BASE_URL = get_secret_or_env("OLLAMA_BASE_URL", "http://localhost:11434")

# General Config 
DATA_DIR = "data/resumes"
REPORTS_DIR = "reports"

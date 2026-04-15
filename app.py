import streamlit as st
import os

# Global configuration
st.set_page_config(
    page_title="SmartHire AI | ATS System",
    page_icon="💼",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Initialize Session State Variables required globally
if "workflow_state" not in st.session_state:
    st.session_state.workflow_state = {
        "jd_text": "",
        "job_description": None,
        "resume_files": [],
        "candidates": [],
        "match_results": [],
        "email_logs": [],
        "error": None
    }

# --- Sidebar: Model Settings ---
with st.sidebar:
    st.header("Model Settings")
    
    # Provider Selection
    current_provider = os.getenv("LLM_PROVIDER", "gemini").lower()
    provider_options = ["Gemini", "Groq", "Ollama"]
    provider_index = 0
    if current_provider in [p.lower() for p in provider_options]:
        provider_index = [p.lower() for p in provider_options].index(current_provider)
    
    llm_provider = st.selectbox("LLM Provider", provider_options, index=provider_index)
    os.environ["LLM_PROVIDER"] = llm_provider.lower()
    
    if llm_provider == "Gemini":
        gemini_key = st.text_input("Google API Key", value=os.getenv("GOOGLE_API_KEY", ""), type="password")
        if gemini_key:
            os.environ["GOOGLE_API_KEY"] = gemini_key
        st.info("Limit: 15 Requests per minute")
            
    elif llm_provider == "Groq":
        groq_key = st.text_input("Groq API Key", value=os.getenv("GROQ_API_KEY", ""), type="password")
        if groq_key:
            os.environ["GROQ_API_KEY"] = groq_key
        st.info("High-speed inference provider")

    elif llm_provider == "Ollama":
        st.text_input("Ollama Base URL", value=os.getenv("OLLAMA_BASE_URL", "http://localhost:11434"), key="ollama_url")
        st.info("Self-hosted local inference")

    st.divider()

# Professional Styling (CSS)
st.markdown("""
<style>
    .stApp {
        background-color: #0F172A;
        color: #F8FAFC;
    }
    .main .block-container {
        padding-top: 3rem;
    }
    h1, h2, h3 {
        font-family: 'Inter', 'Segoe UI', sans-serif;
        color: #F8FAFC;
        font-weight: 600;
        letter-spacing: -0.02em;
    }
    h1 {
        color: #818CF8;
        border-bottom: 2px solid #1E293B;
        padding-bottom: 10px;
        margin-bottom: 20px;
    }
    .metric-card {
        background-color: #1E293B;
        border-radius: 12px;
        padding: 24px;
        box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.1);
        border: 1px solid #334155;
    }
    .stMetric {
        background-color: #1E293B;
        padding: 15px;
        border-radius: 8px;
        border: 1px solid #334155;
    }
    .skill-chip {
        display: inline-block;
        padding: 4px 10px;
        margin: 3px;
        border-radius: 6px;
        font-size: 0.8em;
        font-weight: 500;
        background-color: #334155;
        color: #CBD5E1;
        border: 1px solid #475569;
    }
    .skill-chip.matched {
        background-color: #064E3B;
        border-color: #059669;
        color: #A7F3D0;
    }
    .skill-chip.missing {
        background-color: #7F1D1D;
        border-color: #DC2626;
        color: #FECACA;
    }
    .stButton>button {
        border-radius: 6px;
        font-weight: 500;
        background-color: #4F46E5;
        color: white;
        border: none;
        padding: 0.5rem 1rem;
        transition: background-color 0.2s;
    }
    .stButton>button:hover {
        background-color: #4338CA;
        border: none;
        color: white;
    }
</style>
""", unsafe_allow_html=True)

# Navigation Menu
pages = {
    "Setup": [
        st.Page("pages/jd_upload.py", title="Design Job Description"),
        st.Page("pages/resume_upload.py", title="Import Resumes"),
    ],
    "Analysis & Ranking": [
        st.Page("pages/ranking_dashboard.py", title="Ranking Dashboard"),
        st.Page("pages/candidate_insights.py", title="Candidate Insights"),
        st.Page("pages/analytics_page.py", title="Hiring Analytics"),
    ],
    "Communication": [
        st.Page("pages/email_logs.py", title="Communication Logs"),
    ]
}

pg = st.navigation(pages)
pg.run()

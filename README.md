# SmartHire AI

An end-to-end AI Applicant Tracking System built with Python, Streamlit, LangGraph, and FAISS.

## Features
- **Job Description Parsing**: Uses Google Gemini to extract structured arrays from text/PDF job descriptions.
- **Bulk Resume Upload**: Extracts raw text via PyMuPDF/pdfplumber and maps it into Pydantic models.
- **AI Matching Engine**: 
  - Uses HuggingFace `all-MiniLM-L6-v2` locally via FAISS.
  - Generates scores for Semantics, Skills, Experience, Education, and Projects.
- **LangGraph Multi-Agent Workflow**: Orchestrates the entire pipeline from upload to email auto-sending.
- **Explainable AI Insights**: Shows exactly why a candidate was shortlisted/rejected.
- **Email Automation**: Automatic interview invites and rejections via Python SMTP.

## Installation

1. Create a virtual environment:
```bash
python -m venv venv
venv\\Scripts\\activate
```

2. Install requirements:
```bash
pip install -r requirements.txt
```

3. Configure `.env` using `.env.example`:
```
GOOGLE_API_KEY=your_key_here
SMTP_EMAIL=your_email
SMTP_PASSWORD=your_app_password
```

## Running the App
```bash
streamlit run app.py
```

## Free Deployment (Streamlit Community Cloud)

To deploy this app for free and share the URL:

1. **GitHub**: Create a new repository on GitHub and push this code (ensure `.env` is NOT pushed).
2. **Streamlit Cloud**: Sign in to [share.streamlit.io](https://share.streamlit.io).
3. **Deploy**: 
   - Click "New app".
   - Select your repository and `app.py` as the main file.
4. **Secrets**: 
   - Go to "Settings" -> "Secrets" in the Streamlit Cloud dashboard.
   - Paste your `.env` variables there (e.g., `GOOGLE_API_KEY = "your_key"`).
5. **Share**: Once deployed, you will get a Public URL (e.g., `smarthire-ai.streamlit.app`) to share!

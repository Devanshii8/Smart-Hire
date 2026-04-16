# 🚀 SmartHire AI: Intelligent Applicant Tracking System

<div align="center">
  <img src="https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white"/>
  <img src="https://img.shields.io/badge/Streamlit-FF4B4B?style=for-the-badge&logo=Streamlit&logoColor=white"/>
  <img src="https://img.shields.io/badge/FAISS-1E88E5?style=for-the-badge&logo=Meta&logoColor=white"/>
  <img src="https://img.shields.io/badge/Gemini-8E75B2?style=for-the-badge&logo=google&logoColor=white"/>
  <br/><br/>
  <a href="https://smart-hire-project.streamlit.app/">
    <img src="https://img.shields.io/badge/Live_App-Launch_Web_Application-success?style=for-the-badge&logo=streamlit" alt="Live App Link">
  </a>
</div>

---

## 🎓 Academic Group Project

This project was developed as a comprehensive academic group assignment under the esteemed guidance of **Dr. Arpit Khandelwal**. 

### 👥 Team Members
* **Devanshi Gupta**
* **Tanisha**
* **Aastha**

---

## 🎯 Overview
**SmartHire AI** is an end-to-end Applicant Tracking System (ATS) built to automate and optimize the resume screening process. Utilizing state-of-the-art Large Language Models and mathematically robust Vector Search engines, our system aims to eliminate human bias and drastically reduce the time it takes HR professionals to filter and analyze job applicants.

By leveraging specialized AI agents (via Google Gemini) and mathematical Vector Matching (HuggingFace + FAISS), the application:
- Intelligently parses Job Descriptions alongside unstructured PDF resumes.
- Automatically calculates and scores candidate compatibility based on skills, experience, and educational background.
- Presents actionable insights and AI-driven transparent reasoning for its hiring decisions.
- Facilitates the next stage by dispatching automated acceptance/rejection pipeline emails directly to candidates.

---

## ⚙️ Features
* **Resume Parsing & Semantics:** Deep analysis of incoming PDF resumes instead of simple keyword matching.
* **Intelligent Ranking Dashboard:** Candidates are visually ranked against job requirements with specific granular scores.
* **Decision Transparency:** The LLM explains *why* a candidate was ranked highly or poorly.
* **Automated SMTP Integration:** Directly invite top talent to interviews through our seamless one-click email service.
* **Cross-Provider Architecture:** Built to flexibly utilize Google Gemini, Groq, or Local Ollama models natively.

---

## 🔧 Installation & Setup

Follow these steps to safely set up this application locally.

### Prerequisites
1. **Python 3.10+** installed on your system.
2. A Free API Key from [Google AI Studio](https://aistudio.google.com/).

### Step 1: Clone the Repository
```bash
git clone https://github.com/Devanshii8/Smart-Hire.git
cd Smart-Hire
```

### Step 2: Environment Configuration
Create a file named `.env` in the root folder of the project containing your API keys and (optionally) your SMTP configurations to automate emails.
```env
GOOGLE_API_KEY=your_copied_key_here
SMTP_EMAIL=your_email@gmail.com
SMTP_PASSWORD=your_app_password
SMTP_HOST=smtp.gmail.com
SMTP_PORT=587
HR_COMPANY_NAME=SmartHire AI Inc.
```
*(Note for SMTP: If using Gmail, you must generate an "App Password" from your Google Security Settings, not your primary password).*

### Step 3: Launch Local Environment
We highly recommend running this within a virtual environment.
```bash
# 1. Create the Environment
python -m venv venv

# 2. Activate It
venv\Scripts\activate      # Windows
source venv/bin/activate    # Mac/Linux

# 3. Install Dependencies
pip install -r requirements.txt
```

### Step 4: Start the Server!
Ensure you are in the project root directory and the virtual environment is active, then run:
```bash
streamlit run app.py
```
> **⚠️ First-Run Initialization:** The first resume upload processes takes ~15-30 extra seconds to cache the HuggingFace semantic models locally (80MB). Subsequent processing is instantaneous!

---

## ☁️ Streamlit Cloud Deployment

Want to host this securely online? 

1. Ensure the repository is publicly accessible on your GitHub account.
2. Go to [share.streamlit.io](https://share.streamlit.io/).
3. Click **Create App** → Link your `app.py` location and this repository.
4. Go to **Advanced Settings / Secrets** and paste your `.env` formatting there:
   ```toml
   GOOGLE_API_KEY="your_api_key"
   SMTP_EMAIL="email@gmail.com"
   ```
5. Click deploy and your app will be live globally!

---
*Developed with ❤️ as part of our academic commitment to exploring AI automation paradigms.*

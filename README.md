# SmartHire AI

An end-to-end AI Applicant Tracking System built with Python, Streamlit, LangGraph, and FAISS.

## Overview
This application completely automates the resume screening process. It uses specialized AI agents (via Google Gemini) to parse Job Descriptions and unstructured PDF resumes. It then uses a mathematical Vector Matching engine (HuggingFace + FAISS) to calculate how well candidates match the required skills, experience, and education. It handles automated ranking, explains its AI decisions, and can even automatically send acceptance/rejection emails via SMTP.

---

## 🚀 How to Setup and Run This Application (Handover Guide)

Follow these exact steps to set up this application on a new PC. 

### Prerequisites
1. Ensure **Python 3.10+** is installed on your computer.
2. Ensure you have a **Code Editor** (like VS Code) installed.
3. You need to gather your own free AI API keys (detailed below).

### Step 1: Clone the Repository
Open your Terminal or Command Prompt and clone (download) the code from Github to your machine:
```bash
git clone https://github.com/PrinceKumarIITJ/SmartHire-AI.git
cd SmartHire-AI
```

### Step 2: Set Up API Keys
The system requires an API key to communicate with the Google Gemini AI.
1. Go to [Google AI Studio](https://aistudio.google.com/) and generate a free API key.
2. Inside the `SmartHire-AI` folder, locate the file named `.env.example`.
3. Create a copy of this file and rename the copy to strictly `.env`.
4. Open the new `.env` file in your editor and paste your Google key exactly like this:
   `GOOGLE_API_KEY=your_copied_key_here`
5. *(Optional but Recommended)* If you want the system to send automatic interview and rejection emails, fill out the `SMTP_EMAIL` and `SMTP_PASSWORD` fields. (You will need to generate an App Password from your Google Account settings).

### Step 3: Local Installation
It is highly recommended to install the libraries in an isolated virtual environment to prevent messing up your PC's general Python setup.

Run the following commands in your terminal inside the `SmartHire-AI` folder:

**1. Create a safe Python environment:**
```bash
python -m venv venv
```

**2. Activate the environment:**
*If you are using Windows:*
```bash
venv\\Scripts\\activate
```
*If you are using Mac/Linux:*
```bash
source venv/bin/activate
```

**3. Install the dependencies:**
```bash
pip install -r requirements.txt
```
*(Note: This might take a few minutes as it downloads heavy machine-learning libraries. Proceed to the next step once you regain terminal control).*

### Step 4: Run the Application!
Once installation is complete, launch the web dashboard by typing:
```bash
streamlit run app.py
```
Your default web browser will automatically open a new tab containing the **SmartHire AI** interface!

> ⚠️ **Important First-Run Note:** The very first time you process a batch of resumes, it will take an extra 10-30 seconds. The system has to download a local HuggingFace mathematics model (`all-MiniLM-L6-v2`, ~80MB) directly to your PC cache. Every execution after this will be instantaneous and completely offline.

---

## 🌍 Step 5: Free Cloud Deployment (Streamlit Community Cloud)

If you want to host this application securely on the internet so that anyone with a link can use it (without downloading code), follow these steps:

1. **Fork/Upload to your own GitHub Account:**
   - Make sure this exact code repository is pushed to your personal GitHub account. Make sure it is marked as **Public** (otherwise you might run into private repo limits).
   - Ensure your `.env` file is NOT in the Github repository! Only `.env.example` should be there.

2. **Sign up for Streamlit Cloud:**
   - Go to [share.streamlit.io](https://share.streamlit.io/) and click "Continue with GitHub" to log in.

3. **Deploy the App:**
   - Once logged in, click the **"Create app"** button.
   - Choose **"Yup, I have an app"**.
   - In the form:
     - **Repository**: Select your `SmartHire-AI` repository.
     - **Branch**: `main`
     - **Main file path**: `app.py`
   - Click **"Deploy!"** but quickly prepare for the next step.

4. **Add your SECRETS (Crucial Step):**
   - The app will try to deploy but will crash initially because the cloud server does not have your Google API Key.
   - In the lower-right corner of the Streamlit dashboard, click **Manage App** -> **Settings (the three dots ⋮)** -> **Settings**.
   - Go to the **Secrets** tab.
   - Paste the contents of your `.env` file here exactly as it is formatted locally. For example:
     ```toml
     GOOGLE_API_KEY="your_api_key_here"
     SMTP_EMAIL="your_email@gmail.com"
     SMTP_PASSWORD="your_app_password"
     ```
   - Click **Save**. The app will immediately reboot using those secret keys.

5. **Share it!**
   - Streamlit Cloud will run the installation steps defined in `requirements.txt` automatically.
   - Once the loading screen finishes, your app is live! You can share the public URL at the top of your browser with anyone.

import streamlit as st
import os
from agents.workflow import create_workflow
from services.parser import extract_text

st.title("Design Job Description")
st.markdown("Automate your resume screening by providing a detailed job description. SmartHire AI will extract key requirements.")

cola, colb = st.columns([2, 1])

with cola:
    upload_method = st.radio("Provide JD via:", ["Paste Text", "Upload PDF/TXT Document"], label_visibility="collapsed")
    
    jd_raw_text = ""
    if upload_method == "Paste Text":
        jd_raw_text = st.text_area("Paste the Job Description here", height=300, 
                                 placeholder="""Job Title: Senior Python Developer
We are looking for...
Requirements: 
- 5+ years of experience
- Strong Python, LangChain, AWS skills...""")
    else:
        uploaded_jd = st.file_uploader("Upload Job Description", type=['pdf', 'txt'])
        if uploaded_jd:
            if uploaded_jd.name.endswith('.pdf'):
                # Save temp to extract
                os.makedirs("data/resumes", exist_ok=True)
                temp_path = os.path.join("data/resumes", "temp_jd.pdf")
                with open(temp_path, "wb") as f:
                    f.write(uploaded_jd.getbuffer())
                jd_raw_text = extract_text(temp_path)
            else:
                jd_raw_text = uploaded_jd.getvalue().decode("utf-8")

with colb:
    st.info("Tips for best results:\n- Ensure clear skill requirements\n- Mention minimum experience years\n- Specify degree requirements if any")
    
    if st.button("Extract JD Requirements", type="primary", use_container_width=True):
        if len(jd_raw_text) < 20:
            st.error("Please provide a longer job description.")
        else:
            with st.spinner("Analyzing Job Description..."):
                # Save to state
                st.session_state.workflow_state["jd_text"] = jd_raw_text
                
                # We only want to run the first node conceptually, but we can just use the compiled graph
                # and modify the state manually for the specific node logic (or just call the node function).
                from agents.jd_agent import parse_jd_node
                
                result = parse_jd_node(st.session_state.workflow_state)
                
                if "error" in result:
                    st.error(result["error"])
                else:
                    st.session_state.workflow_state["job_description"] = result["job_description"]
                    st.success("Successfully analyzed job description.")

st.divider()

# Display Parsed Results
if st.session_state.workflow_state.get("job_description"):
    jd = st.session_state.workflow_state["job_description"]
    
    st.subheader(f"Extracted Profile: {jd.title}")
    
    c1, c2, c3 = st.columns(3)
    c1.metric("Min. Experience", f"{jd.experience_years} Years")
    c2.metric("Min. Education", jd.education if jd.education else "Not specified")
    c3.metric("Keywords", len(jd.role_keywords))

    st.markdown("#### Must-Have Skills")
    html_must = "".join([f"<span class='skill-chip'>{s}</span>" for s in jd.must_have_skills])
    st.markdown(html_must, unsafe_allow_html=True)
    
    if jd.preferred_skills:
        st.markdown("#### Preferred Skills")
        html_pref = "".join([f"<span class='skill-chip'>{s}</span>" for s in jd.preferred_skills])
        st.markdown(html_pref, unsafe_allow_html=True)
        
    with st.expander("View Raw JD Context"):
        st.write(jd.raw_text)

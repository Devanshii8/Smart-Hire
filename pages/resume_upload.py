import streamlit as st
import os

st.title("Import Applicant Resumes")
st.markdown("Upload multiple PDF resumes. The system will parse them and run them through our AI Matching Engine against the Job Description.")

if not st.session_state.workflow_state.get("job_description"):
    st.warning("Please set up a Job Description first on the Design page.")
    st.stop()

uploaded_files = st.file_uploader("Upload PDF Resumes", type="pdf", accept_multiple_files=True)

if uploaded_files:
    os.makedirs("data/resumes", exist_ok=True)
    
    if st.button("Process Resumes and Run Analysis", type="primary", use_container_width=True):
        saved_paths = []
        with st.spinner("Saving uploaded files..."):
            for file in uploaded_files:
                path = os.path.join("data/resumes", file.name)
                with open(path, "wb") as f:
                    f.write(file.getbuffer())
                saved_paths.append(path)
                
        # Update workflow state
        st.session_state.workflow_state["resume_files"] = saved_paths
        
        # We trigger the workflow natively using LangGraph
        from agents.workflow import create_workflow
        app = create_workflow()
        
        try:
            with st.spinner("Processing analysis workflow..."):
                # Run standard workflow
                state_result = app.invoke(st.session_state.workflow_state)
                
                if "error" in state_result and state_result["error"]:
                    st.error(f"Workflow failed: {state_result['error']}")
                else:
                    # Update global state with final output
                    st.session_state.workflow_state = state_result
                    st.success(f"Successfully processed {len(saved_paths)} resumes.")
                    st.toast("Analysis complete. Check the Ranking Dashboard.")
                    
        except Exception as e:
            st.error(f"Critical error during workflow execution: {e}")

# Display previously parsed candidates
if st.session_state.workflow_state.get("candidates"):
    st.divider()
    st.subheader(f"Extracted Candidates ({len(st.session_state.workflow_state['candidates'])})")
    
    for cand in st.session_state.workflow_state["candidates"]:
        with st.expander(f"{cand.name} - {cand.email}"):
            c1, c2 = st.columns(2)
            c1.write(f"**Experience:** {cand.total_experience_years} years")
            c2.write(f"**Phone:** {cand.phone}")
            
            st.write("**Top Skills:**")
            html_skills = "".join([f"<span class='skill-chip'>{s}</span>" for s in cand.skills[:10]])
            st.markdown(html_skills, unsafe_allow_html=True)

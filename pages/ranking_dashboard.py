import streamlit as st
import pandas as pd
from utils.helpers import format_score
from services.email_service import check_email_config, send_invite_email, send_rejection_email

st.title("Candidate Ranking Dashboard")
st.markdown("Review the AI ranking of candidates compared against the current job requirements.")

if not st.session_state.workflow_state.get("match_results"):
    st.info("No candidates ranked yet. Please upload and process resumes first.")
    st.stop()

results = st.session_state.workflow_state["match_results"]

# Filtering Section
st.subheader("Filters")
col1, col2 = st.columns(2)
with col1:
    min_score_pct = st.slider("Minimum Final Score (%)", 0, 100, 50)
with col2:
    status_filter = st.multiselect("Filter by Status", ["Shortlisted", "Rejected", "Pending"], default=["Shortlisted", "Rejected"])

# Logic for filtering (Ensuring rounding doesn't cause skip)
filtered_results = [
    r for r in results 
    if round(r.final_score * 100, 1) >= min_score_pct and r.status in status_filter
]

# Display Table
if filtered_results:
    data = []
    for i, r in enumerate(filtered_results):
        data.append({
            "Rank": i + 1,
            "Name": r.candidate_name,
            "Score": format_score(r.final_score),
            "Status": r.status,
            "Action Reason": r.reason,
            "Matched": len(r.matched_skills)
        })
    df = pd.DataFrame(data)
    
    # Styled dataframe
    def color_status(val):
        color = '#A7F3D0' if val == 'Shortlisted' else '#FECACA' if val == 'Rejected' else '#CBD5E1'
        return f'color: {color}; font-weight: bold;'
    
    st.dataframe(df.style.map(color_status, subset=['Status']), use_container_width=True)
    
    # Manual Communication Trigger
    st.divider()
    st.subheader("Communication Management")
    c1, c2 = st.columns([2, 1])
    with c1:
        st.write("Send automated updates based on the current AI status.")
        confirm_send = st.checkbox("I have reviewed the candidates and wish to send updates.")
    
    with c2:
        if st.button("Send Invitations", disabled=not confirm_send, type="primary", use_container_width=True):
            if not check_email_config():
                st.error("SMTP Configuration missing. Please check your .env file.")
            else:
                sent_count = 0
                shortlisted = [r for r in filtered_results if r.status == "Shortlisted"]
                with st.spinner("Dispatching emails..."):
                    for r in shortlisted:
                        # Find candidate Profile
                        cand_profile = next((c for c in st.session_state.workflow_state["candidates"] if c.id == r.candidate_id), None)
                        if cand_profile:
                            log = send_invite_email(cand_profile, st.session_state.workflow_state["job_description"].title)
                            st.session_state.workflow_state["email_logs"].append(log)
                            sent_count += 1
                st.success(f"Dispatched {sent_count} invitations successfully.")

    st.divider()
    st.subheader("Decision Reasoning")
    for r in filtered_results:
        with st.expander(f"[{r.status}] #{results.index(r)+1} {r.candidate_name} - {format_score(r.final_score)}"):
            st.markdown(f"**Analysis:** {r.semantic_explanation}")
            
            sc1, sc2, sc3, sc4 = st.columns(4)
            sc1.metric("Semantic Match", format_score(r.semantic_score))
            sc2.metric("Skill Overlap", format_score(r.skill_score))
            sc3.metric("Experience", format_score(r.experience_score))
            sc4.metric("Academic", format_score(r.education_score))

else:
    st.warning("No candidates match the current filters.")

# Secondary Actions
st.divider()
from services.analytics import generate_csv_report
if st.button("Download CSV Report"):
    csv_path = generate_csv_report(results)
    with open(csv_path, "rb") as f:
        st.download_button("Export as CSV", f, file_name="rankings_report.csv", mime="text/csv")

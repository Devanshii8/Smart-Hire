from langchain_core.documents import Document
from services.embeddings import build_faiss_index, query_faiss, get_embedding_model
from services.scoring import (
    compute_skill_overlap, compute_experience_score,
    compute_education_score, compute_project_relevance,
    extract_matched_missing_skills
)
from utils.models import WorkflowState, MatchResult
import numpy as np

def match_node(state: WorkflowState) -> dict:
    """
    LangGraph Node: Calculates semantic match using FAISS and structured scores.
    """
    print("Agent: Matching starting...")
    candidates = state.get("candidates", [])
    jd = state.get("job_description")
    
    if not jd or not candidates:
        return {"error": "Missing JD or Candidates for matching."}

    # Prepare candidate texts for FAISS
    # We embed the raw text of the resume
    docs = []
    for c in candidates:
        docs.append(Document(page_content=c.raw_text, metadata={"id": c.id}))

    # Build FAISS index
    index = build_faiss_index(docs)
    
    # Query with JD
    query_text = jd.raw_text if jd.raw_text else " ".join(jd.must_have_skills + jd.role_keywords)
    
    # Get L2 distances for all candidates
    faiss_results = query_faiss(index, query_text, k=len(candidates))
    
    # Create mapping from candidate_id to L2 distance
    # Lower L2 distance = higher similarity
    l2_scores = {res[0].metadata["id"]: res[1] for res in faiss_results}
    
    # Normalize L2 distance to a 0.0 - 1.0 similarity score
    if l2_scores:
        max_d = max(l2_scores.values()) if max(l2_scores.values()) > 0 else 1
        semantic_scores = {cid: 1 - (dist / max_d) for cid, dist in l2_scores.items()}
    else:
        semantic_scores = {}

    match_results = []
    for c in candidates:
        # 1. Semantic Score
        sem_score = semantic_scores.get(c.id, 0.0)
        
        # 2. Skill Overlap
        skill_ovlp = compute_skill_overlap(c.skills, jd.must_have_skills)
        matched, missing = extract_matched_missing_skills(c.skills, jd.must_have_skills)
        
        # 3. Experience Match
        exp_score = compute_experience_score(c.total_experience_years, jd.experience_years)
        
        # 4. Education Match
        edu_score = compute_education_score(c.education, jd.education)
        
        # 5. Project Relevance
        proj_score = compute_project_relevance(c.projects, jd.role_keywords)

        mr = MatchResult(
            candidate_id=c.id,
            candidate_name=c.name,
            candidate_email=c.email,
            semantic_score=sem_score,
            skill_score=skill_ovlp,
            experience_score=exp_score,
            education_score=edu_score,
            project_score=proj_score,
            matched_skills=matched,
            missing_skills=missing
        )
        match_results.append(mr)

    return {"match_results": match_results}

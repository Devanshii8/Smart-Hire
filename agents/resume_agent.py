from langchain_core.prompts import PromptTemplate
from services.llm_factory import get_llm
from utils.models import WorkflowState, CandidateProfile
from utils.prompts import RESUME_PARSE_PROMPT
from utils.helpers import safe_json_parse, compute_hash, sanitize_name
from services.parser import extract_text
import os
import time

def parse_resumes_node(state: WorkflowState) -> dict:
    """
    LangGraph Node: Reads PDF resumes, extracts text, calls LLM, and structured CandidateProfiles.
    Handles deduplication via hash.
    """
    print("Agent: Resume Parser starting...")
    resume_files = state.get("resume_files", [])
    existing_candidates = state.get("candidates", [])
    
    if not resume_files:
        return {"error": "No resumes provided for parsing."}

    llm = get_llm()
    prompt = PromptTemplate(template=RESUME_PARSE_PROMPT, input_variables=["text"])
    chain = prompt | llm

    # Deduplication map
    processed_hashes = {c.id for c in existing_candidates}
    new_candidates = []

    for file_path in resume_files:
        try:
            file_hash = compute_hash(file_path)
            if file_hash in processed_hashes:
                print(f"Skipping duplicate: {file_path}")
                continue

            print(f"Parsing: {file_path}")
            raw_text = extract_text(file_path)
            
            if not raw_text or len(raw_text) < 50:
                print(f"Could not extract meaningful text from {file_path}")
                continue

            # API Rate limit safety for batching
            time.sleep(2) 
            
            response = chain.invoke({"text": raw_text})
            parsed_dict = safe_json_parse(response.content)
            
            # Map back essential attributes
            parsed_dict["id"] = file_hash
            parsed_dict["filename"] = os.path.basename(file_path)
            parsed_dict["raw_text"] = raw_text
            parsed_dict["name"] = sanitize_name(parsed_dict.get("name", "Unknown"))
            
            candidate = CandidateProfile(**parsed_dict)
            new_candidates.append(candidate)
            processed_hashes.add(file_hash)
            
        except Exception as e:
            print(f"Error processing {file_path}: {e}")

    # Merge previously processed with newly processed
    all_candidates = existing_candidates + new_candidates
    return {"candidates": all_candidates}

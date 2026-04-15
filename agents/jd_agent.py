from services.llm_factory import get_llm
from langchain_core.prompts import PromptTemplate
from utils.models import WorkflowState, JobDescription
from utils.prompts import JD_PARSE_PROMPT
from utils.helpers import safe_json_parse
import os

def parse_jd_node(state: WorkflowState) -> dict:
    """
    LangGraph Node: Parses raw job description text into structured JSON using the selected LLM.
    """
    print("Agent: JD Parser starting...")
    jd_text = state.get("jd_text", "")
    
    if not jd_text:
        return {"error": "No Job Description text provided."}

    llm = get_llm()
    prompt = PromptTemplate(template=JD_PARSE_PROMPT, input_variables=["text"])
    
    chain = prompt | llm
    
    try:
        response = chain.invoke({"text": jd_text})
        parsed_dict = safe_json_parse(response.content)
        
        # Keep raw text for embedding later
        parsed_dict["raw_text"] = jd_text
        jd = JobDescription(**parsed_dict)
        
        return {"job_description": jd}
        
    except Exception as e:
        print(f"Error parsing JD: {e}")
        return {"error": f"Failed to parse JD: {str(e)}"}

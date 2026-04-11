from fsm.states import NEXT
from prompts.chains import get_chain
from prompts.judge_chain import get_judge_chain
from utils.utils import sanitize
from llm.model import llm_judge
import json
# 1. Update llm_gate buat nerima last_question
'''def llm_gate(stage, stage_buffer):
    judge_chain = get_judge_chain(stage, llm_judge)
    
    response = judge_chain.invoke({
        "text": stage_buffer
    })
    
    try:
        raw = response.content.strip()
        raw = raw.replace("```json", "").replace("```", "").strip()
        result = json.loads(raw)
    except:
        result = {
            "verdict": "stay",
            "fulfilled": [],
            "missing": ["tidak bisa parsing response judge"]
        }
    
    return result'''

def llm_gate(stage, stage_buffer):
    judge_chain = get_judge_chain(stage, llm_judge)
    
    response = judge_chain.invoke({"text": stage_buffer})
    
    print("=== JUDGE RAW OUTPUT ===")
    print(response.content)
    print("========================")
    
    try:
        raw = response.content.strip()
        raw = raw.replace("```json", "").replace("```", "").strip()
        result = json.loads(raw)
    except Exception as e:
        print(f"=== PARSING ERROR: {e} ===")
        result = {
            "verdict": "stay",
            "fulfilled": [],
            "missing": []
        }
    
    print(f"=== VERDICT: {result} ===")
    return result

# 2. Update fsm_step buat nerima last_question
def fsm_step(stage, full_history, llm, stage_buffer, last_question, last_user_input):

    # Oper last_question ke llm_gate
    decision = llm_gate(stage, stage_buffer)
    verdict = decision.get("verdict", "stay").lower()
    missing = decision.get("missing",[])
    
    new_stage = NEXT[stage] if decision == "advance" else stage
    if new_stage=="completed":
        return new_stage, None, stage_buffer, decision

    if verdict == "advance":
        stage_buffer = ""
        missing = []

    # Generate pertanyaan baru berdasarkan stage (yang mungkin sudah update)
    chain = get_chain(new_stage, llm, full_history, stage_buffer, missing)
    
    new_question = sanitize(chain.invoke({
        "stage_buffer": stage_buffer,
        "full_history": full_history
    }).content)

    return new_stage, new_question, stage_buffer, decision
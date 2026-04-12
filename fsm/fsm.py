from fsm.states import NEXT
from prompts.chains import get_chain
from prompts.judge_chain import get_judge_chain
from utils.utils import sanitize
from llm.model import llm_judge
import json

# 1. Update llm_gate buat nerima last_question
def llm_gate(stage, stage_buffer):
    judge_chain = get_judge_chain(stage, llm_judge)
    
    response = judge_chain.invoke({"text": stage_buffer})
    
    try:
        raw = response.content.strip()
        raw = raw.replace("```json", "").replace("```", "").strip()
        result = json.loads(raw)
    except Exception as e:
        result = {
            "verdict": "stay",
            "fulfilled": [],
            "missing": []
        }
    
    return result

# 2. Update fsm_step buat nerima last_question
def fsm_step(stage, full_history, llm, stage_buffer, last_user_input=""):
    loop_count = len(stage_buffer.strip().split("\n")) if stage_buffer else 0
    MAX_LOOP = 5
    decision = llm_gate(stage, stage_buffer)
    verdict = decision.get("verdict", "stay").lower()
    missing = decision.get("missing", [])
    
    if verdict == "advance":
        new_stage = NEXT[stage]
    elif loop_count >= MAX_LOOP and verdict=="stay":
        new_stage = NEXT[stage]
    else:
        new_stage = stage
    
    if new_stage == "completed":
        return new_stage, None, stage_buffer, decision

    if verdict == "advance":
        stage_buffer = ""
        missing = []

    chain = get_chain(new_stage, llm, full_history, stage_buffer, missing, last_user_input)
    new_question = sanitize(chain.invoke({}).content)

    return new_stage, new_question, stage_buffer, decision
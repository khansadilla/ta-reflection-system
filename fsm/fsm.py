from fsm.states import NEXT
from prompts.chains import get_chain
from prompts.judge_chain import get_judge_chain
from utils.utils import sanitize
from llm.model import llm_judge

# 1. Update llm_gate buat nerima last_question
def llm_gate(stage, stage_buffer, last_question):
    judge_chain = get_judge_chain(stage, llm_judge)
    
    # Kirim dua-duanya ke judge_chain
    response = judge_chain.invoke({
        "text": stage_buffer, 
        "question": last_question
    })
    
    decision = response.content.strip().replace(".", "").replace(" ", "").lower()
    return decision

# 2. Update fsm_step buat nerima last_question
def fsm_step(stage, full_history, llm, stage_buffer, last_question, last_user_input):

    # Oper last_question ke llm_gate
    decision = llm_gate(stage, last_user_input, last_question)
    
    new_stage = NEXT[stage] if decision == "advance" else stage
    if new_stage=="completed":
        return new_stage, None, stage_buffer, decision

    if decision == "advance":
        stage_buffer = ""

    # Generate pertanyaan baru berdasarkan stage (yang mungkin sudah update)
    chain = get_chain(new_stage, llm, full_history, stage_buffer)
    
    new_question = sanitize(chain.invoke({
        "stage_buffer": stage_buffer,
        "full_history": full_history
    }).content)

    return new_stage, new_question, stage_buffer, decision
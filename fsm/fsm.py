from fsm.states import NEXT
from prompts.chains import get_chain
from prompts.judge_chain import get_judge_chain
from utils.sanitize import sanitize
from llm.model import llm_judge

def llm_gate(stage, stage_buffer):

    judge_chain = get_judge_chain(stage, llm_judge)
    decision = judge_chain.invoke({"text": stage_buffer}).content.strip()
    decision = decision.replace(".", "")
    decision = decision.replace(" ", "")
    return decision.lower()

def fsm_step(stage, full_history, llm, stage_buffer):

    decision = llm_gate(stage, stage_buffer)
    new_stage = NEXT[stage] if decision=="advance" else stage

    if decision=="advance":
        stage_buffer=""

    chain = get_chain(new_stage, llm, full_history, stage_buffer)
    question = sanitize(chain.invoke({
        "stage_buffer":stage_buffer,
        "full_history":full_history
    }).content
    )

    return new_stage, question, stage_buffer, decision

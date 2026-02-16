from fsm.states import NEXT
from prompts.chains import get_chain
from utils.sanitize import sanitize

def gate(state, text):
    return "advance" if len(text.strip())>20 else "stay"

def fsm_step(stage, user_text, llm):
    decision = gate(stage, user_text)
    new_stage = NEXT[stage] if decision=="advance" else stage

    chain = get_chain(new_stage, llm)
    question = sanitize(chain.invoke({"text": user_text}).content)

    return new_stage, question
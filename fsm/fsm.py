from fsm.states import NEXT
from prompts.chains import get_chain
from prompts.judge_chain import get_judge_chain
from utils.sanitize import sanitize
from llm.model import llm_judge

'''def gate(stage, text):
    cleaned = text.strip().lower()

    if(stage=="reporting_responding"):
        temporal_markers=["kemarin","tadi","waktu itu","dulu","sejak","pas","akhir-akhir ini"]
        emotion_markers=["sedih","bahagia","senang","marah","takut","kecewa","stres","lega","bersalah"]
        action_markers=["ngerjain","bilang","ngobrol","ketemu","presentasi","baca","bikin","mulai","selesai","putus"]

        has_temporal = any(m in cleaned for m in temporal_markers)
        has_emotion = any(m in cleaned for m in emotion_markers)
        has_action = any(m in cleaned for m in action_markers)    

        score=has_temporal+has_emotion+has_action

        if(score<2):
            return "stay"


    if(stage=="reasoning"):
        reasoning_markers=["karena aku","aku jadi"]

        if not any(m in cleaned for m in reasoning_markers):
            return "stay"

    return "advance" if len(text.strip())>20 else "stay"'''

def llm_gate(stage, stage_buffer):

    judge_chain = get_judge_chain(stage, llm_judge)
    decision = judge_chain.invoke({"text": stage_buffer}).content.strip()
    decision = decision.replace(".", "")
    decision = decision.replace(" ", "")
    return decision.lower()

def fsm_step(stage, user_text, llm, stage_buffer):

    stage_buffer+="\n"+user_text.strip()
    
    decision = llm_gate(stage, stage_buffer)
    new_stage = NEXT[stage] if decision=="advance" else stage

    if decision=="advance":
        stage_buffer=""

    chain = get_chain(new_stage, llm, stage_buffer)
    question = sanitize(chain.invoke({"text": user_text}).content)

    return new_stage, question, stage_buffer

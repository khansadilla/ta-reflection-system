from llm.model import llm_judge
from rag.knowledge_base import transition_indicators
from langchain_core.prompts import ChatPromptTemplate

def format_indicators(stage):
    indicators = transition_indicators.get(stage,{})

    advance = "\n".join([f"-{i}" for i in indicators.get("advance_if",[])])
    stay = "\n".join([f"-{i}" for i in indicators.get("stay_if",[])])

    return f""" KRITERIA ADVANCE: {advance} \n KRITERIA STAY: {stay}"""
    

def get_judge_chain(stage, llm_judge):

    indikator_text = format_indicators(stage)

    prompt = ChatPromptTemplate.from_messages([
        (
            "system",
            f"""
            Kamu adalah evaluator refleksi berbasis 5R.

            Tentukan apakah respons pengguna sudah cukup untuk naik tahap.

            Penting:
            - Gunakan penilaian semantik, bukan hanya pencocokan kata literal.
            - Respons tidak harus panjang untuk dianggap mendalam.
            - Jika secara makna sudah memenuhi kriteria advance, jawab ADVANCE.

            {indikator_text}

            Jika memenuhi KRITERIA ADVANCE → jawab ADVANCE.
            Jika tidak → jawab STAY.

            Output hanya satu kata.
            """
        ),
        (
            "human",
            "{text}"
        )
    ])

    return prompt | llm_judge

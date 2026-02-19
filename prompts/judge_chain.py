from llm.model import llm_judge
from rag.retriever import format_indicators
from langchain_core.prompts import ChatPromptTemplate

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

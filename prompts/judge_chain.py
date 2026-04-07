from llm.model import llm_judge
from rag.knowledge_base import transition_indicators
from langchain_core.prompts import ChatPromptTemplate
from fsm.states import NEXT

def format_indicators(stage):
    indicators = transition_indicators.get(stage,{})

    advance = "\n".join([f"-{i}" for i in indicators.get("advance_if",[])])
    stay = "\n".join([f"-{i}" for i in indicators.get("stay_if",[])])

    return f""" KRITERIA ADVANCE: {advance} \n KRITERIA STAY: {stay}"""
    

def get_judge_chain(stage, llm_judge):

    next

    indikator_text = format_indicators(stage)

    prompt = ChatPromptTemplate.from_messages([
        (
            "system",
            f"""
            Kamu adalah classifier refleksi berbasis 5R.

            Tahap saat ini: {stage}

            Tugasmu: memutuskan apakah respons pengguna sudah cukup untuk pindah ke tahap berikutnya.

            Gunakan penilaian semantik.

            {indikator_text}
            
            Aturan keputusan:
            - Jika memenuhi KRITERIA ADVANCE → ADVANCE
            - Jika tidak → STAY

            ADVANCE jika jawaban sudah cukup memenuhi kriteria advance.

            Aturan OUTPUT (WAJIB):
            -Output harus tepat satu kata
            -Hanya boleh: ADVANCE atau STAY
            -Jangan menjelaskan alasan
            -Jangan menulis kalimat lain
            -Jangan menambah tanda baca

            Contoh output benar:
            ADVANCE
            STAY
            """
        ),
        (
            "human",
            f"""
                TAHAP REFLEKSI: {stage}

                ### KONTEKS PERCAKAPAN
                Pertanyaan Sistem: {{question}}
                Respons Pengguna: {{text}}

                Berdasarkan konteks di atas, apakah respons pengguna sudah memenuhi kriteria untuk lanjut? 
                Keputusan:
                """
        )
    ])

    return prompt | llm_judge

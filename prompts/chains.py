from langchain_core.prompts import ChatPromptTemplate

from prompts.instructions import core_instruction, stage_instruction
from rag.retriever import retrieve

def get_chain(stage, llm, full_history, stage_buffer):

    knowledge = retrieve(stage, stage_buffer, k=2)
    instruction = core_instruction() + stage_instruction(stage)

    prompt = ChatPromptTemplate.from_messages([
        (
            "system",instruction
        ),
        (
           "human",f"""
            Riwayat percakapan:
            {full_history}

            Input terbaru:
            {stage_buffer}

            Context tambahan (REFERENSI SAJA, BUKAN FAKTA USER):
            {knowledge}

            ATURAN PENGGUNAAN CONTEXT:
            - Jangan menganggap context sebagai kondisi user.
            - Gunakan hanya jika ADA KECocokan eksplisit dengan ucapan user.
            - Jika tidak ada kecocokan, abaikan sepenuhnya.

            INSTRUKSI UTAMA:
            - Fokus utama tetap pada kata-kata user.
            - Jika informasi kurang, bertanya, bukan menyimpulkan.
            - Semua insight harus bisa dilacak ke ucapan user.
            """
        )
    ])

    return prompt | llm
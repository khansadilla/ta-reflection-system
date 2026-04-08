from langchain_core.prompts import ChatPromptTemplate
from prompts.instructions import core_instruction, stage_instruction
from rag.retriever import retrieve
from utils.utils import get_recent_history
def get_chain(stage, llm, full_history, stage_buffer):

    knowledge = retrieve(stage, stage_buffer, k=2)
    instruction = core_instruction() + stage_instruction(stage)

    recent_history = get_recent_history(full_history)

    prompt = ChatPromptTemplate.from_messages([
        (
            "system",instruction
        ),
        (
           "human",    f"""

            ATURAN MEMBACA KONTEKS:
            - Gunakan RIWAYAT hanya untuk memahami alur percakapan
            - Gunakan INPUT TERBARU sebagai titik masuk
            - Gunakan FOKUS REFLEKSI untuk memahami makna yang lebih dalam
            

            FOKUS REFLEKSI SAAT INI (inti pembahasan):
            - Ini adalah kumpulan pemikiran user yang menunjukkan arah refleksi
            - Gunakan ini untuk memahami pola atau makna yang sedang berkembang
            {stage_buffer}

            INPUT TERBARU:
            {stage_buffer.split("\n")[-1]}
            
            RIWAYAT PERCAKAPAN (untuk menjaga alur):
            {recent_history}

            ATURAN PERCAKAPAN:
            - Jangan memulai ulang percakapan
            - Jangan menyapa seperti percakapan baru
            - Langsung lanjut dari konteks yang ada

            ATURAN ANALISIS:
            - Semua insight harus bisa dilacak ke ucapan user
            - Jangan mengasumsikan hal yang tidak dikatakan
            - Jika informasi kurang → bertanya, bukan menyimpulkan
            """
        )
    ])

    return prompt | llm
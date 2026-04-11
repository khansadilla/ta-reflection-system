from langchain_core.prompts import ChatPromptTemplate
from prompts.instructions import core_instruction, stage_instruction
from utils.utils import get_recent_history
def get_chain(stage, llm, full_history, stage_buffer, missing):
    
    recent_history = get_recent_history(full_history)

    missing_text = "\n".join(f"- {m}" for m in missing) if missing else "tidak ada"

    prompt = ChatPromptTemplate.from_messages([
        (
            "system",f"""
            STAGE INSTRUCTION:
            {stage_instruction(stage)}

            CORE INSTRUCTION
            {core_instruction()}
            """
        ),
        (
           "human",    f"""

            ATURAN MEMBACA KONTEKS:
            - Gunakan RIWAYAT hanya untuk memahami alur percakapan
            - Gunakan FOKUS REFLEKSI untuk memahami makna yang lebih dalam

            YANG BELUM DIGALI (fokus ke salah satu ini!):
            {missing_text}

            FOKUS REFLEKSI SAAT INI:
            {stage_buffer}

            INPUT TERBARU:
            {stage_buffer.split(chr(10))[-1]}

            RIWAYAT PERCAKAPAN:
            {recent_history}

            ATURAN PERCAKAPAN:
            - Jangan memulai ulang percakapan
            - Langsung lanjut dari konteks yang ada
            - Fokus pertanyaan ke YANG BELUM DIGALI di atasan
            - Jika informasi kurang → bertanya, bukan menyimpulkan
            """
        )
    ])

    return prompt | llm
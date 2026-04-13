from langchain_core.prompts import ChatPromptTemplate
from prompts.instructions import core_instruction, stage_instruction
from utils.utils import get_recent_history

PRIORITY_MAP = {
    "reporting_responding": ["Situasi", "Emosi", "Respon"],
    "relating": ["Faktor internal", "Pola"],
    "reasoning": ["Insight", "Perubahan cara pandang", "Dampak"],
    "reconstructing": ["Tindakan spesifik", "Konteks", "Alasan"]
}

MISSING_GUIDE = {
    "Situasi": "arahkan ke memperjelas apa yang terjadi",
    "Emosi": "arahkan ke apa yang dirasakan",
    "Respon": "arahkan ke apa yang dilakukan atau dipikirkan",

    "Pola": "cek apakah ini sering terjadi",
    "Faktor internal": "arahkan ke penyebab dari dalam diri",

    "Insight": "dorong ke pemahaman baru yang lebih jelas",
    "Perubahan cara pandang": "arahkan ke pergeseran perspektif",
    "Dampak": "gali pengaruhnya ke diri",

    "Tindakan spesifik": "minta aksi yang konkret",
    "Konteks": "minta kapan atau bagaimana dilakukan",
    "Alasan": "tanya kenapa ini akan membantu"
}

def sort_missing(stage, missing):
    priority = PRIORITY_MAP.get(stage, [])
    return sorted(
        missing,
        key=lambda x: priority.index(x) if x in priority else 999
    )

def get_chain(stage, llm, full_history, stage_buffer, missing=None, last_user_input=""):
    sorted_missing = sort_missing(stage, missing) if missing else []
    primary_missing = sorted_missing[0] if sorted_missing else None
    focus_text = primary_missing if primary_missing else "tidak ada"
    guide_text = MISSING_GUIDE.get(primary_missing, "")

    recent_history = get_recent_history(full_history)

    if not primary_missing:
        focus_text = "lanjutkan eksplorasi dari konteks"
        guide_text = "perdalam bagian yang paling menarik dari pembicaraan"

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
            "human", f"""


            RIWAYAT PERCAKAPAN:
            {recent_history}

            FOKUS REFLEKSI (akumulasi di stage ini):
            {stage_buffer}

            INPUT TERBARU:
            {last_user_input}

            FOKUS UTAMA:
            {focus_text}

            ARAH PERTANYAAN:
            {guide_text}

            ATURAN:
            - Langsung lanjut dari konteks yang ada
            - Fokus utama ke FOKUS UTAMA
            - Gunakan arah pertanyaan sebagai panduan, bukan diulang mentah
            - Jangan menanyakan lebih dari satu hal
            """
        )
    ])

    return prompt | llm
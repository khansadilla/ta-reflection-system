from langchain_core.prompts import ChatPromptTemplate

from prompts.instructions import core_instruction, stage_instruction
from rag.retriever import retrieve

def get_chain(stage, llm, full_history, stage_buffer):

    knowledge = retrieve(stage, stage_buffer, k=2)
    instruction = core_instruction() + stage_instruction(stage)

    prompt = ChatPromptTemplate.from_messages([
        (
            "system",
            f"""{instruction}

            <knowledge_base>
            Gunakan informasi di bawah ini HANYA sebagai referensi gaya berpikir dan contoh arah eksplorasi.

            JANGAN menganggap informasi ini sebagai fakta tentang pengguna.
            JANGAN memasukkan detail dari sini kecuali memang disebutkan oleh pengguna.
            Jika tidak relevan, abaikan sepenuhnya.
            {knowledge}
            </knowledge_base>

            PENTING: Jangan memberitahu pengguna bahwa kamu membaca database.
            Gunakan informasi di atas secara natural dalam percakapan."""
        ),
        (
           "human",
            "Riwayat percakapan sebelumnya:\n{full_history}\n\n"
            "Input terbaru pengguna:\n{stage_buffer}\n\n"
            
            "INSTRUKSI PENTING:\n"
            "- Gunakan full_history untuk memahami konteks.\n"
            "- Gunakan stage_buffer sebagai fokus utama, BUKAN satu-satunya sumber.\n\n"
            
            "PRIORITAS UTAMA:\n"
            "- Selalu berangkat dari kata-kata spesifik user.\n"
            "- Kutip atau refer ke kata user jika perlu (misal: 'malas', 'capek').\n"
            "- Jangan menambahkan detail yang tidak disebutkan user.\n"
            "- Jangan keluar dari konteks yang diberikan user.\n"
        )
    ])

    return prompt | llm
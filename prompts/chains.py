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
            Gunakan informasi di bawah ini sebagai pedoman operasional dan inspirasi pertanyaan:
            {knowledge}
            </knowledge_base>

            PENTING: Jangan memberitahu pengguna bahwa kamu membaca database.
            Gunakan informasi di atas secara natural dalam percakapan."""
        ),
        (
            "human",
            "Riwayat percakapan sebelumnya:\n{full_history}\n\n"
            "Input terbaru pengguna (fokus pada tahap ini):\n{stage_buffer}"
        )
    ])

    return prompt | llm
from langchain_core.prompts import ChatPromptTemplate

from prompts.instructions import core_instruction, stage_instruction
from rag.retriever import retrieve

def get_chain(stage, llm, stage_buffer):

    knowledge = retrieve(stage, stage_buffer, k=2)
    instruction = core_instruction() + stage_instruction(stage)

    prompt = ChatPromptTemplate.from_messages([
        (
            "system",
            f"{knowledge}\n\n{instruction}"
        ),
        (
            "human",
            "{text}"
        )
    ])

    return prompt | llm
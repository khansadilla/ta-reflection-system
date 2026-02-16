from langchain_core.prompts import ChatPromptTemplate

from prompts.instructions import core_instruction, stage_instruction
from rag.retriever import get_knowledge

def get_chain(stage, llm):

    knowledge = get_knowledge(stage)
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
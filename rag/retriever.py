from rag.knowledge_base import knowledge_base

def get_knowledge(stage):
    kb = knowledge_base.get(stage, {})
    parts = []

    for section in ["goal", "guidance", "reflective_pitfalls"]:
        parts.extend(kb.get(section, []))

    return "\n".join(parts)

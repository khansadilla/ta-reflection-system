from rag.knowledge_base import knowledge_base, transition_indicators

def get_knowledge(stage):
    kb = knowledge_base.get(stage, {})
    parts = []

    for section in ["goal", "guidance", "reflective_pitfalls"]:
        parts.extend(kb.get(section, []))

    return "\n".join(parts)

def format_indicators(stage):
    indicators = transition_indicators.get(stage, {})
    
    advance = "\n".join([f"- {i}" for i in indicators.get("advance_if", [])])
    stay = "\n".join([f"- {i}" for i in indicators.get("stay_if", [])])

    return f"""
            KRITERIA ADVANCE:
            {advance}

            KRITERIA STAY:
            {stay}
            """

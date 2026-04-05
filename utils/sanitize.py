def sanitize(text):
    lines = [l.strip() for l in text.split("\n") if l.strip()]
    return "\n".join(lines)
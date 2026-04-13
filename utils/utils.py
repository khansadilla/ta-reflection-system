def sanitize(text):
    lines = [l.strip() for l in text.split("\n") if l.strip()]
    return "\n".join(lines)

def get_recent_history(full_history, n=4):
    lines = full_history.strip().split("\n")
    return "\n".join(lines[-n:])


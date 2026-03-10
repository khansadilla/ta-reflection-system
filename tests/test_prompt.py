from fsm.fsm import fsm_step
from llm.model import llm

stage = "reporting_responding"
stage_buffer = ""

test_inputs = [
    "kemarin aku presentasi dan aku merasa kecewa",
    "ini mirip kayak waktu aku gagal lomba dulu",
    "mungkin aku terlalu butuh validasi",
    "mulai minggu depan aku mau bikin jadwal lebih terstruktur",
]

def lexical_overlap(input_text, question):
    input_words = set(input_text.lower().split())
    question_words = set(question.lower().split())
    return len(input_words.intersection(question_words))


def run_prompt_test():
    global stage, stage_buffer

    grounded = 0
    total = 0

    print("\n===== PROMPT BASELINE =====\n")

    for text in test_inputs:
        stage, question, stage_buffer = fsm_step(stage, text, llm, stage_buffer)

        overlap = lexical_overlap(text, question)
        is_grounded = overlap > 0

        if is_grounded:
            grounded += 1

        total += 1

        print("Input:", text)
        print("Question:", question)
        print("Lexical Overlap:", overlap)
        print("-" * 50)

    print("\nGrounded Rate:", grounded / total)
    print("Manual Task: Beri skor Cognitive Push (1–5) untuk tiap pertanyaan.\n")


if __name__ == "__main__":
    run_prompt_test()
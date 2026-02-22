from prompts.chains import get_chain
from llm.model import llm

test_inputs = [
    "aku sering menunda karena takut gagal",
    "aku bingung antara idealisme dan ekspektasi orang tua",
    "aku capek jadi perfeksionis",
    "aku merasa tidak dihargai di tim",
    "aku takut masa depanku tidak jelas"
]

def is_generic(question: str):
    generic_patterns = [
        "apa yang kamu rasakan",
        "bagaimana perasaanmu",
        "apa yang kamu pikirkan",
        "apa yang membuatmu merasa"
    ]

    q = question.lower()
    return any(p in q for p in generic_patterns)

def run_tests():
    print("\n===== DIRECT REASONING TEST =====\n")

    total = 0
    non_generic = 0

    for i, text in enumerate(test_inputs, 1):

        chain = get_chain("reasoning", llm, text)
        question = chain.invoke({"text": text}).content.strip()

        print(f"Test {i}")
        print("Input     :", text)
        print("Question  :", question)

        total += 1

        if not is_generic(question):
            non_generic += 1
            print("Depth     : OK (non-generic)")
        else:
            print("Depth     : GENERIC")

        print("-" * 60)

    print("\n===== SUMMARY =====")
    print(f"Non-generic reasoning: {non_generic} / {total}")
    print("=====================\n")

if __name__ == "__main__":
    run_tests()
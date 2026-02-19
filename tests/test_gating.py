from fsm.fsm import llm_gate

# =====================================================
# REALISTIC / MESSY / BORDERLINE TEST CASES
# =====================================================

test_cases = [

    # =================================================
    # REPORTING_RESPONDING (Messy)
    # =================================================
    ("reporting_responding",
     "kemarin ada apa ya pokoknya ribet deh",
     "stay"),

    ("reporting_responding",
     "kemarin presentasi, aku deg deg an banget soalnya dosennya diem aja",
     "advance"),

    ("reporting_responding",
     "aku kesel sih",
     "stay"),

    ("reporting_responding",
     "tadi aku ketemu dia di kampus dan aku jadi kepikiran terus",
     "advance"),

    # =================================================
    # RELATING (Messy & Borderline)
    # =================================================
    ("relating",
     "aku jadi mikir aku juga gitu sih kadang",
     "advance"),  # ada koneksi ke diri sendiri

    ("relating",
     "ya gitu aja sih",
     "stay"),

    ("relating",
     "ini mirip sama waktu aku semester 5 dulu, aku juga sering nunda",
     "advance"),

    ("relating",
     "mungkin ini sering kejadian",
     "stay"),

    # =================================================
    # REASONING (Borderline)
    # =================================================
    ("reasoning",
     "mungkin dia stres karena tekanan",
     "advance"),  # minimal sebab-akibat

    ("reasoning",
     "ya dia stres aja sih",
     "stay"),

    ("reasoning",
     "kayaknya bukan cuma stres, tapi dia takut dinilai gagal jadi dia menghindar",
     "advance"),

    ("reasoning",
     "soalnya skripsi itu berat",
     "stay"),

    # =================================================
    # RECONSTRUCTING (Messy)
    # =================================================
    ("reconstructing",
     "ya nanti coba ngobrol deh",
     "stay"),  # terlalu vague

    ("reconstructing",
     "aku bakal ajak dia bikin target mingguan biar lebih terstruktur",
     "advance"),

    ("reconstructing",
     "semoga aja dia sadar",
     "stay"),

    ("reconstructing",
     "mulai minggu depan aku akan cek progresnya tiap Jumat sore",
     "advance"),
]


def run_tests():
    print("\n===== REALISTIC GATING TEST START =====\n")

    correct = 0

    for i, (stage, text, expected) in enumerate(test_cases, 1):

        decision = llm_gate(stage, text)
        decision = decision.strip().lower().replace(".", "")
        decision = decision.split()[0]

        result = "PASS" if decision == expected else "FAIL"

        if result == "PASS":
            correct += 1

        print(f"Test {i}")
        print("Stage     :", stage)
        print("Input     :", text)
        print("Expected  :", expected)
        print("Decision  :", decision)
        print("Result    :", result)
        print("-" * 60)

    print("\n===== SUMMARY =====")
    print(f"{correct} / {len(test_cases)} tests passed")
    print("===================\n")


if __name__ == "__main__":
    run_tests()

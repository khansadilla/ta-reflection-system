from fsm.fsm import gate

stage = "reasoning"

test_cases = [
    ("Aku capek banget.","stay"),
    ("Aku capek karena tugasnya banyak.","stay"),
    ("Aku perfeksionis banget.","stay"),
    ("Aku capek jadi.","stay"),
    ("Aku capek karena aku capek.","advance"),
    ("Aku capek karena aku terlalu perfeksionis dan selalu memaksakan diri.","advance"),
    ("Aku jadi burnout karena aku selalu takut gagal dan tidak bisa berhenti.","advance"),
    ("Aku jadi stres karena aku merasa harus selalu memenuhi ekspektasi orang.","advance"),
    ("Aku capek karena aku merasa produktivitas adalah nilai diriku.","advance"),
    ("Aku jadi gampang marah karena aku terlalu menekan diri sendiri.","advance"),
    ("Karena aku takut gagal, aku jadi keras ke diri sendiri.","stay"),
    ("Aku capek jadi aku overwork terus.","stay"),
    ("Aku sering overthink jadi aku burnout.","stay")
]

for text, expected in test_cases:
    result = gate(stage, text)
    print(text)
    print("Expected:", expected)
    print("Actual", result)

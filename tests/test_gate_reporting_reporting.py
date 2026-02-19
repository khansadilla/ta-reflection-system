from fsm.fsm import gate

stage = "reporting_responding"

test_cases = [
    # ❌ HARUS STAY (0 atau 1 kategori saja)

    ("aku lagi bahagia banget","stay"),  # hanya emosi
    ("kemarin aku ada sesuatu","stay"),  # hanya waktu
    ("aku presentasi tadi","stay"),  # hanya aksi
    ("aku merasa hidupku berubah","stay"),  # abstrak, tidak ada waktu jelas
    ("aku senang","stay"),  # terlalu pendek dan hanya emosi
    ("pas itu aku bingung","stay"),  # waktu + emosi? tergantung 'bingung' masuk list atau tidak


    # ✅ HARUS ADVANCE (2 dari 3 atau 3 dari 3)

    ("akhir-akhir ini aku merasa bahagia","advance"),  # waktu + emosi
    ("kemarin aku presentasi TA","advance"),  # waktu + aksi
    ("aku merasa tegang pas presentasi","advance"),  # emosi + waktu/aksi
    ("kemarin aku presentasi dan aku merasa sangat tegang","advance"),  # semua 3
    ("aku stres sejak kemarin","advance"),  # emosi + waktu
    ("pas ngobrol sama dia aku merasa kecewa","advance"),  # waktu + aksi + emosi
    ("minggu ini aku mulai ngerjain TA dan aku merasa lega","advance"),  # semua 3


    # ⚠️ EDGE / AMBIGUOUS

    ("akhir-akhir ini aku berubah","stay"),  # waktu saja
    ("aku mulai merasa lebih baik","stay"),  # aksi + emosi (tergantung 'mulai' & 'merasa' masuk list)
    ("sejak dulu aku bahagia","advance"),  # waktu + emosi
]


for text, expected in test_cases:
    result = gate(stage, text)
    print(text)
    print("Expected:", expected)
    print("Actual:", result)

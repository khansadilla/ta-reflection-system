from langchain_core.documents import Document

def build_documents():
    docs = []
    # Mengambil data dari dictionary knowledge_base
    for stage, content in knowledge_base.items():
        # SESUAIKAN DISINI: Pakai kunci baru sesuai Tabel IV.2
        categories = ["pedoman", "bank_pertanyaan", "contoh_penalaran", "korpus"]
        
        for section in categories:
            # Pakai .get() supaya kalau ada kunci yang typo nggak error
            texts = content.get(section, [])
            for text in texts:
                docs.append(
                    Document(
                        page_content=text,
                        metadata={
                            "stage": stage,
                            "type": section # Tambahkan type biar sesuai proposal
                        }
                    )
                )
    return docs

knowledge_base = {
    "reporting_responding": {
        "pedoman": [
            "Goal: Deskripsi kejadian & reaksi emosi. Gunakan PAST TENSE (Saya menyadari, Saya merasa).",
            "Kunci: Fokus ke 'Apa yang terjadi?' dan 'Gimana perasaanmu saat itu?'.",
            "Note: Reporting & Responding bisa digabung buat flow yang lebih natural."
        ],
        "bank_pertanyaan": [
            "Dari semua kejadian tadi, momen mana sih yang paling jadi 'puncak' atau paling bikin kamu kepikiran?",
            "Pas momen itu terjadi, apa hal pertama yang langsung lewat di pikiran atau perasaanmu?",
            "Kalau kejadian ini difilmkan, adegan mana yang menurutmu paling krusial buat dibahas?",
            "Apa sih yang bikin kamu ngerasa [emosi user] pas situasi itu berlangsung?"
        ],
        "korpus": [
            "Gue ngerasa stuck banget, kayak usaha gue selama ini gak ada progress-nya.",
            "Asli, tadi pas presentasi gue nge-blank parah padahal udah latihan.",
            "Lagi ngerasa hampa, kayak gak tau arah tujuannya mau ke mana."
        ]
    },
    "relating": {
        "pedoman": [
            "Goal: Hubungkan ke pola lama/skill. Gunakan PRESENT TENSE (Ini mengingatkan saya pada...).",
            "Kunci: Cari koneksi antara 'sekarang' dengan 'pengalaman masa lalu' atau 'siapa saya'."
        ],
        "bank_pertanyaan": [
            "Pernah nggak kamu ngerasa di posisi yang mirip kayak gini sebelumnya? Kapan itu?",
            "Ini 'lagu lama' yang keulang lagi atau emang tantangan baru yang beda banget buat kamu?",
            "Gimana kejadian ini mencerminkan kebiasaan kamu selama ini kalau lagi dapet masalah serupa?",
            "Apa bedanya cara kamu nanggepin hal ini sekarang dibanding kamu yang versi 1-2 tahun lalu?"
        ]
    },
    "reasoning": {
        "pedoman": [
            "Goal: Analisis sebab-akibat & faktor signifikan. Gunakan PRESENT TENSE (Saya memahami bahwa...).",
            "Kunci: Cari faktor internal/eksternal. Pakai bahasa analitis (mengimplikasikan, faktor kuncinya)."
        ],
        "bank_pertanyaan": [
            "Menurutmu, apa faktor paling 'X' atau paling penting yang bikin situasi ini terjadi?",
            "Kalau kita liat dari kacamata orang lain yang terlibat, kenapa ya mereka bersikap kayak gitu?",
            "Apa sih faktor tersembunyi yang mungkin bikin kamu ngerasa se-overwhelmed ini?",
            "Gimana pemahaman baru ini ngebantu kamu ngelihat masalahnya secara lebih jelas?"
        ]
    },
    "reconstructing": {
        "pedoman": [
            "Goal: Rencana aksi konkret (Future Plan). Gunakan FUTURE TENSE (Saya akan, Selanjutnya...).",
            "Kunci: Harus realistis (SMART) dan didukung oleh pemahaman dari tahap sebelumnya."
        ],
        "bank_pertanyaan": [
            "Kalau besok kejadian lagi, apa satu hal kecil yang mau kamu coba lakuin secara berbeda?",
            "Satu langkah paling kecil yang bisa kamu lakuin 5 menit dari sekarang apa nih?",
            "Apa 'mantra' atau pengingat baru yang mau kamu tanemin biar pola yang sama nggak keulang?",
            "Apa yang bakal terjadi kalau kamu nyoba pendekatan [opsi baru] buat masalah ini?"
        ]
    }
}

transition_indicators = {

    "reporting_responding": {
        "advance_if": [
            "Respons menunjukkan pola diri atau generalisasi diri",
            "Respons menyatakan bahwa situasi tersebut sering terjadi atau berulang"
        ],
        "stay_if": [
            "Respons hanya mendeskripsikan kejadian atau emosi",
            "Tidak ada indikasi pola atau kebiasaan diri"
        ]
    },

    "relating": {
        "advance_if": [
            "Respons mengajukan hipotesis tentang penyebab pola tersebut",
            "Respons mencoba menjelaskan mengapa pola itu terjadi"
        ],
        "stay_if": [
            "Respons hanya menyebut pola tanpa menjelaskan sebab",
            "Tidak ada upaya menjelaskan mengapa pola itu terjadi"
        ]
    },

    "reasoning": {
        "advance_if": [
            "Respons menunjukkan insight atau pemahaman baru tentang diri",
            "Respons menunjukkan perubahan cara pandang terhadap situasi"
        ],
        "stay_if": [
            "Respons hanya memberikan hipotesis sebab tanpa insight baru",
            "Tidak ada perubahan pemahaman tentang diri"
        ]
    },

    "reconstructing": {
        "advance_if": [
            "Respons menyusun rencana tindakan atau langkah konkret ke depan"
        ],
        "stay_if": [
            "Respons hanya menyebut insight tanpa rencana tindakan"
        ]
    }
}

if __name__ == "__main__":
    from rag.retriever import embeddings # Pastikan import embeddings-nya bener
    from langchain_community.vectorstores import FAISS
    
    # Fungsi build_documents yang sudah kamu punya sebelumnya
    documents = build_documents() 
    
    print("Building FAISS vectorstore...")
    vectorstore = FAISS.from_documents(documents, embeddings)
    vectorstore.save_local("rag/vectorstore")
    print("Vectorstore berhasil dibuat! Sekarang jalankan lagi retriever.py-nya.")

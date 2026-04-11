from langchain_core.prompts import ChatPromptTemplate
def get_summary_chain(llm, full_history):
    prompt = ChatPromptTemplate.from_messages([
        (
            "system",
            """
            Kamu adalah teman refleksi yang hangat.
            Tugas: Buat ringkasan refleksi user dengan gaya yang supportif dan personal.
            
            STRUKTUR RINGKASAN:
            1. Apa yang terjadi (singkat)
            2. Insight utama yang ditemukan user
            3. Rencana aksi yang sudah disusun
            4. Kalimat penutup yang menyemangati
            
            GAYA:
            - Hangat, seperti teman
            - Pakai "kamu" bukan "Anda"
            - Jangan terlalu panjang
            """
        ),
        (
            "human",
            f"Berikut adalah percakapan refleksi:\n{full_history}"
        )
    ])
    
    return prompt | llm
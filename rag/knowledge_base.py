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
            "Fokus pada deskripsi kejadian secara objektif: Apa, Siapa, Di mana, Kapan.",
            "Gali reaksi emosional spontan (gut feeling) yang muncul saat kejadian.",
            "Validasi perasaan user tanpa menghakimi (non-judgmental validation).",
            "Identifikasi konflik utama: Apakah masalah teknis, interpersonal, atau internal?",
            "Gunakan 'paraphrasing' untuk memastikan bot paham inti masalah user.",
            "Hindari memberikan saran di tahap ini; biarkan user menuangkan emosinya.",
            "Gunakan pertanyaan terbuka (Open-ended questions) untuk memperluas cerita.",
            "Cari 'titik balik' atau momen paling intens dalam cerita user.",
            "Observasi bahasa tubuh (jika diceritakan) atau nada bicara dalam teks.",
            "Tujuannya adalah menciptakan ruang aman (safe space) bagi user."
        ],
        "bank_pertanyaan": [
            "Momen mana sih yang paling bikin kamu kepikiran dari kejadian tadi?",
            "Apa hal pertama yang langsung lewat di pikiranmu pas itu terjadi?",
            "Gimana reaksi tubuhmu saat itu? (Misal: sesak, deg-degan, atau lemas?)",
            "Kalau kejadian ini difilmkan, adegan mana yang menurutmu paling krusial?",
            "Apa sih yang sebenernya paling kamu takutin dari situasi ini?",
            "Siapa orang yang paling berpengaruh dalam momen yang kamu ceritain tadi?",
            "Kalau kamu harus kasih satu judul buat perasaanmu sekarang, apa judulnya?",
            "Apa ekspektasimu di awal sebelum kejadian ini akhirnya berantakan?",
            "Bisa ceritain lebih detail soal bagian yang bikin kamu ngerasa 'stuck' itu?",
            "Gimana perasaanmu berubah dari awal kejadian sampai akhirnya kamu cerita ke aku?"
        ],
        "contoh_penalaran": [
            "User merasa bersalah karena menganggap kegagalan tim adalah tanggung jawab pribadinya.",
            "Respon emosional user berupa kemarahan sebenarnya adalah bentuk frustrasi atas hal yang tidak bisa dikontrol.",
            "User mengalami kecemasan sosial yang dipicu oleh feedback negatif dari figur otoritas.",
            "Kelelahan yang dialami user bukan hanya fisik, tapi juga mental karena beban kognitif yang tinggi."
        ],
        "korpus": [
            "Aku ngerasa hampa banget, skripsi nggak jalan padahal udah di depan laptop seharian.",
            "Tadi dapet feedback pedes dari dosen, rasanya pengen nyerah aja hari ini.",
            "Asli, tadi pas presentasi gue nge-blank parah padahal udah latihan seminggu.",
            "Lagi ngerasa lari di tempat sementara temen-temen udah pada sidang.",
            "Gue kesel sama diri sendiri karena malah main game pas deadline udah mepet.",
            "Rasanya kayak nggak ada progres sama sekali, padahal aku udah usaha keras.",
            "Tadi debat sama temen kelompok, rasanya nggak enak banget sampai sekarang.",
            "Aku takut banget ditanya progres sama ortu, rasanya pengen ngilang aja.",
            "Lagi ngerasa nggak kompeten, kayaknya aku salah ambil jurusan deh.",
            "Pikiran aku berisik banget, isinya cuma skenario terburuk yang bakal terjadi."
        ]
    },
    "relating": {
        "pedoman": [
            "Cari hubungan (connection) antara masalah sekarang dengan pengalaman masa lalu.",
            "Identifikasi apakah ini adalah 'pola perilaku' (pattern) yang sering berulang.",
            "Hubungkan masalah dengan nilai-nilai pribadi atau standar kesuksesan user.",
            "Cari kemiripan emosi: 'Kapan lagi saya pernah merasa seperti ini?'.",
            "Gunakan analogi untuk memperjelas keterkaitan masalah.",
            "Evaluasi apakah skill yang user punya sekarang sudah cukup untuk menghadapi ini.",
            "Fokus pada identitas diri: 'Bagaimana kejadian ini mencerminkan siapa saya?'.",
            "Bandingkan respon user sekarang dengan cara mereka menangani masalah dulu.",
            "Tujuannya adalah kesadaran diri (self-awareness) atas pola hidup.",
            "Gali keterkaitan antara masalah profesional/akademik dengan masalah personal."
        ],
        "bank_pertanyaan": [
            "Pernah nggak kamu ngerasa di posisi yang mirip kayak gini sebelumnya? Kapan?",
            "Ini 'lagu lama' yang keulang lagi atau tantangan yang bener-bener baru buat kamu?",
            "Gimana cara kamu yang dulu menangani hal mirip ini? Berhasil nggak?",
            "Apakah rasa 'nggak pantes' ini sering muncul di situasi lain selain skripsi?",
            "Apa bedanya kamu yang sekarang menghadapi ini dibanding kamu yang 2 tahun lalu?",
            "Kejadian ini ngingetin kamu sama momen apa di masa sekolah atau organisasi?",
            "Kalau liat ke belakang, apa persamaan antara semua masalah yang pernah bikin kamu 'stuck'?",
            "Seberapa sering kamu ngerasa harus 'sempurna' sebelum berani mulai sesuatu?",
            "Apakah pola komunikasi ini juga muncul pas kamu lagi sama keluarga atau teman?",
            "Apa satu kelebihanmu yang biasanya membantu di situasi sulit, tapi sekarang kayaknya 'tidur'?"
        ],
        "contoh_penalaran": [
            "User menyadari bahwa sifat perfeksionismenya selalu muncul saat menghadapi tugas yang tidak terstruktur.",
            "Ketakutan user pada dosen penguji berakar dari pengalaman masa kecil dengan figur otoritas yang keras.",
            "User melihat pola bahwa ia cenderung menarik diri (withdraw) setiap kali menghadapi konflik interpersonal."
        ],
        "korpus": [
            "Ini mirip pas aku ikut organisasi dulu, aku sering nunda karena takut hasilnya jelek.",
            "Rasa nggak layak ini tuh sebenernya udah ada dari jaman aku ikut olimpiade SMA.",
            "Biasanya kalau aku stuck, aku bakal ghosting semua orang. Sama kayak sekarang.",
            "Dulu aku pernah gagal di lomba, dan rasanya persis kayak kegagalan skripsi ini.",
            "Aku baru sadar kalau aku selalu cari validasi orang lain biar ngerasa aman.",
            "Kejadian ini persis kayak pas aku magang, aku takut nanya karena takut dianggap bego.",
            "Pola overthinking ini emang udah jadi 'teman setia' aku dari dulu kalau ada tekanan.",
            "Dulu aku bisa handle masalah ini dengan cara kerja keras sampai tipes, tapi sekarang nggak bisa.",
            "Aku sadar kalau aku sering naruh standar yang terlalu tinggi buat diriku sendiri.",
            "Ini ngingetin aku pas aku hampir telat lulus SMA karena males ngerjain tugas akhir."
        ]
    },
    "reasoning": {
        "pedoman": [
            "Lakukan analisis sebab-akibat (Root Cause Analysis).",
            "Bedah faktor internal (sifat, kebiasaan, mindset) yang memperkeruh masalah.",
            "Bedah faktor eksternal (sistem, orang lain, lingkungan) secara objektif.",
            "Gunakan perspektif orang ketiga untuk meminimalisir bias emosional.",
            "Cari literatur atau teori yang bisa menjelaskan fenomena yang dialami user.",
            "Evaluasi konsekuensi jangka pendek dan jangka panjang dari situasi tersebut.",
            "Tantang asumsi atau 'limiting beliefs' yang dimiliki oleh user.",
            "Tujuannya adalah menemukan insight atau pemahaman baru (Aha! Moment).",
            "Hubungkan berbagai faktor yang terlihat acak menjadi satu kesimpulan logis.",
            "Fokus pada pertanyaan 'Mengapa' dan 'Bagaimana bisa demikian'."
        ],
        "bank_pertanyaan": [
            "Menurutmu, apa 3 faktor paling utama yang bikin situasi ini makin rumit?",
            "Kalau kita liat dari kacamata dosenmu, kenapa ya beliau bersikap kayak gitu ke kamu?",
            "Apa sih faktor 'tersembunyi' (hidden factor) yang mungkin belum kamu sadari sebelumnya?",
            "Gimana pemahaman baru ini ngebantu kamu ngelihat masalahnya secara lebih jernih?",
            "Apa sih konsekuensi paling buruk yang logis kalau skripsi ini telat? (Coba bedah asumsimu).",
            "Kenapa menurutmu strategi yang kamu pake sekarang nggak berhasil mengatasi 'males' itu?",
            "Seberapa besar pengaruh lingkungan belajarmu terhadap produktivitasmu saat ini?",
            "Kalau kamu jadi pengamat luar, saran apa yang bakal kamu kasih buat orang di posisimu?",
            "Apa kaitan antara ketakutanmu akan sidang dengan cara kamu nyiapin materinya?",
            "Apa sih yang sebenernya bikin dosen itu jadi keliatan 'menakutkan' buat kamu?"
        ],
        "contoh_penalaran": [
            "Masalah utama bukan pada kemampuan akademik, melainkan pada kecemasan akan penilaian orang lain (fear of judgment).",
            "Dosen bersikap keras mungkin karena ingin menjaga kualitas lulusan, bukan karena ketidaksukaan personal.",
            "User memahami bahwa 'prokrastinasi' adalah cara otak menghindari emosi negatif terkait tugas tersebut."
        ],
        "korpus": [
            "Setelah dipikir, faktor utamanya adalah aku terlalu peduli sama omongan orang lain.",
            "Kayaknya dosenku gitu karena emang standarnya tinggi, bukan karena benci aku personal.",
            "Aku sadar kalau aku nunda karena aku nggak tahu harus mulai dari paragraf mana.",
            "Ternyata aku takut lulus karena aku takut menghadapi dunia kerja yang nggak pasti.",
            "Faktor eksternalnya emang lingkunganku lagi toxic banget, jadi aku nggak fokus.",
            "Aku paham sekarang kalau 'males' itu sebenernya cuma tameng karena aku takut gagal.",
            "Ternyata cara bimbinganku salah, aku harusnya lebih proaktif nanya, bukan nunggu.",
            "Insight-nya adalah: aku butuh struktur yang jelas biar nggak ngerasa overwhelmed.",
            "Aku baru sadar kalau aku nggak punya support system yang beneran ngerti aku.",
            "Ternyata selama ini aku cuma 'sibuk' tapi nggak 'produktif', ada bedanya ya."
        ]
    },
    "reconstructing": {
        "pedoman": [
            "Susun rencana aksi masa depan yang konkret dan terukur (Future Plan).",
            "Fokus pada perubahan perilaku kecil (Small Wins) untuk membangun momentum.",
            "Gunakan pemahaman dari tahap Reasoning untuk mencegah pola yang sama.",
            "Terapkan strategi antisipasi: 'Jika X terjadi, saya akan melakukan Y'.",
            "Tingkatkan 'Sense of Agency' user agar mereka merasa mampu melakukan perubahan.",
            "Evaluasi sumber daya apa yang dibutuhkan untuk menjalankan rencana baru.",
            "Buat target yang realistis dan ramah terhadap kesehatan mental (SMART goals).",
            "Tujuannya adalah transformasi diri dan perbaikan berkelanjutan.",
            "Gunakan 'mantra' atau pengingat untuk menjaga konsistensi rencana.",
            "Pastikan rencana aksi didukung oleh bukti bahwa user punya kemampuan itu."
        ],
        "bank_pertanyaan": [
            "Kalau besok situasi ini keulang, apa 1 hal paling kecil yang mau kamu coba lakuin beda?",
            "Langkah paling kecil apa yang bisa kamu ambil dalam 15 menit ke depan?",
            "Apa 'mantra' atau pengingat baru yang mau kamu tanemin biar pola lama nggak keulang?",
            "Gimana kamu bakal ngerayain kalau kamu berhasil nulis satu paragraf hari ini?",
            "Apa rencana cadanganmu kalau ternyata besok kamu ngerasa males lagi?",
            "Siapa orang yang bisa kamu ajak diskusi atau minta bantuan buat jaga konsistensimu?",
            "Apa satu kebiasaan buruk yang mau kamu 'pensiunkan' mulai hari ini?",
            "Bisa buatkan jadwal yang sangat sederhana buat besok pagi? (Max 3 kegiatan).",
            "Apa yang bakal kamu bilang ke dirimu sendiri pas nanti rasa takut itu muncul lagi?",
            "Gimana cara kamu memastikan kalau rencana aksi ini beneran realistis buat kamu jalanin?"
        ],
        "contoh_penalaran": [
            "User memutuskan untuk menggunakan teknik Pomodoro agar tidak terbebani durasi kerja yang lama.",
            "User merancang 'check-list' harian yang sangat kecil untuk membangun rasa percaya diri kembali.",
            "User akan melakukan simulasi sidang mandiri untuk mengurangi kecemasan saat bertemu dosen."
        ],
        "korpus": [
            "Besok aku mau coba nulis 100 kata aja, nggak usah nunggu mood bagus.",
            "Aku bakal coba ajak temen buat 'deep work' bareng biar ada yang ngawasin aku.",
            "Mulai besok aku mau batasin buka medsos sebelum target nulis harian selesai.",
            "Aku mau coba buat draf pertanyaan bimbingan semalam sebelum ketemu dosen.",
            "Setiap ngerasa takut, aku mau tarik napas dan bilang: 'Satu langkah kecil dulu'.",
            "Aku bakal buat jadwal istirahat yang bener, biar nggak burn out terus nunda lagi.",
            "Besok pagi aku mau mulai benerin daftar pustaka dulu, yang gampang-gampang aja.",
            "Aku mau jujur ke dosen soal kendalaku, kayaknya komunikasi itu kuncinya.",
            "Aku bakal coba aplikasi blocker buat HP-ku selama jam ngerjain skripsi.",
            "Minggu depan aku targetin bab 3 ini harus beres, gimanapun hasilnya."
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

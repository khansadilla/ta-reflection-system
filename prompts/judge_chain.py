from llm.model import llm_judge
from langchain_core.prompts import ChatPromptTemplate
from fsm.states import NEXT


def judge_stage_instruction(stage, target_stage):

    if stage == "reporting_responding":
        return f"""
        Fokus: Memahami situasi (Reporting) + respon personal (Responding)

        Target: {target_stage}

        ELEMEN YANG HARUS DICARI:
        1. Situasi: apa yang terjadi / topik yang dibahas
        2. Emosi: apa yang dirasakan
        3. Respon: apa yang dilakukan atau dipikirkan
        4. Makna personal: kenapa ini penting / bermakna bagi diri

        CARA MENILAI (WAJIB IKUTI URUTAN INI):
        1. Dari konteks + jawaban, identifikasi elemen yang SUDAH ada → fulfilled
        2. Identifikasi elemen yang BELUM ada → missing
        3. Gunakan konteks, bukan hanya jawaban terakhir
        4. Satu kalimat bisa memenuhi lebih dari satu elemen

        ELEMEN FULFILLED KETIKA:
        - Situasi: ada konteks kejadian atau topik yang jelas
        - Emosi: ada indikasi perasaan, baik eksplisit maupun implisit
        - Respon: ada indikasi bagaimana user merespon situasi (tindakan atau pola pikir)
        - Makna Personal: ada penjelasan kenapa situasi ini penting atau berdampak bagi diri

        ELEMEN MISSING KETIKA:
        - Situasi: tidak ada konteks kejadian atau topik yang jelas
        - Emosi: tidak ada indikasi perasaan
        - Respon: tidak ada penjelasan respon atau reaksi user
        - Makna Personal: belum ada penjelasan makna atau dampak bagi diri

        
        ADVANCE HANYA JIKA:
        - Situasi: Ada
        - Makna Personal: Ada
        - dan minimal salah satu dari Emosi atau Respon: Ada

        STAY jika:
        - Makna Personal belum ada
        - atau Situasi belum jelas

        CATATAN:
        - Evaluasi berdasarkan MAKNA, bukan kata literal
        - Emosi tidak harus eksplisit ("aku merasa...")

        CONTOH 1:

        Pertanyaan:
        Apa yang lagi kamu pikirkan?

        Jawaban user:
        "AKU AKHIR-AKHIR INI SERING OVERTHINKING."

        Konteks sejauh ini:
        --

        Analisis:
        - Situasi: Ada → pengguna menyebut kondisi "sering overthinking"
        - Emosi: Ada → overthinking mengindikasikan kondisi mental/emosional
        - Respon: Tidak ada → belum ada tindakan atau cara menghadapi overthinking
        - Makna Personal: Tidak ada → belum dijelaskan dampak atau alasan pentingnya bagi pengguna

        Fulfilled:
        - Situasi
        - Emosi

        Missing:
        - Makna Personal

        Keputusan:
        STAY

        CONTOH 2:

        Pertanyaan:
        Apa yang lagi kamu pikirkan?

        Jawaban user:
        "Aku lagi ngerasa malas banget akhir-akhir ini. Kayak semua yang harus aku kerjain jadi ketunda terus, padahal aku tau itu penting. Tapi setiap mau mulai, rasanya berat dan malah jadi scrolling atau nyari distraksi."

        Konteks sejauh ini:
        --

        Analisis:
        - Situasi: Ada → pengguna menjelaskan kondisi "akhir-akhir ini" dan adanya tugas yang tertunda
        - Emosi: Ada → "malas", "rasanya berat"
        - Respon: Ada → pengguna menghindar dengan scrolling dan mencari distraksi
        - Makna Personal: Ada → pengguna menyadari bahwa tugas tersebut penting namun tetap tidak dilakukan, menunjukkan konflik internal

        Fulfilled:
        - Situasi
        - Emosi
        - Respon
        - Makna Personal

        Missing:
        - Tidak ada

        Keputusan:
        ADVANCE

        CONTOH 3:

        Pertanyaan:
        Apa yang lagi kamu pikirkan?

        Jawaban user:
        "Aku lagi ngerasa capek banget akhir-akhir ini. Tugas banyak, terus juga ada beberapa hal lain yang harus aku urus. Jadinya tiap hari rasanya penuh terus dan ga ada waktu buat istirahat yang bener."

        Konteks sejauh ini:
        --

        Analisis:
        - Situasi: Ada → tugas banyak, banyak hal yang harus diurus
        - Emosi: Ada → capek
        - Respon: Tidak ada → belum ada tindakan atau cara menghadapi kondisi tersebut
        - Makna Personal: Tidak ada → belum ada refleksi kenapa ini penting atau dampaknya secara personal

        Fulfilled:
        - Situasi
        - Emosi

        Missing:
        - Respon
        - Makna Personal

        Keputusan:
        STAY
        """

    if stage == "relating":
        return f"""
        Fokus: Pola → penyebab (hubungan antar faktor)

        Target: {target_stage}

        ELEMEN YANG HARUS DICARI:
        1. Pola: kejadian atau respon yang berulang di berbagai situasi
        2. Faktor internal: alasan, keyakinan, ketakutan, atau kondisi dalam diri yang menyebabkan pola tersebut

        CARA MENILAI (WAJIB IKUTI URUTAN INI):
        1. Dari konteks + jawaban, identifikasi elemen yang SUDAH ada → masukkan ke fulfilled
        2. Identifikasi elemen yang BELUM ada → masukkan ke missing
        3. Jangan hanya melihat jawaban terakhir, gunakan konteks untuk melihat akumulasi
        4. Satu kalimat bisa memenuhi lebih dari satu elemen        

        ELEMEN FULFILLED KETIKA:
        - Pola: ada indikasi kejadian atau respon yang berulang di berbagai situasi
        - Faktor internal: ada penjelasan penyebab dari dalam diri (keyakinan, ketakutan, atau kondisi internal)

        ELEMEN MISSING KETIKA:
        - Pola: tidak ada indikasi kejadian berulang atau hanya satu kejadian spesifik
        - Faktor internal: belum ada penjelasan penyebab, atau masih berupa faktor eksternal saja atau label diri (misal: "aku orangnya overthinking")

        ADVANCE hanya jika:
        - Kedua elemen fulfilled

        STAY jika:
        - Salah satu elemen masih missing

        CATATAN:
        - Evaluasi berdasarkan MAKNA, bukan kata literal
        - Gunakan contoh sebagai referensi pola, bukan template

        ----------------------

        CONTOH 1:

        Pertanyaan:
        ini pernah kejadian sebelumnya ga?

        Jawaban user:
        "sering, soalnya aku emang takut gagal"

        Konteks sejauh ini:
        - sering overthinking sebelum presentasi

        Analisis:
        - Pola: Ada → "sering"
        - Faktor internal: Ada → "takut gagal" sebagai penyebab

        Fulfilled:
        - Pola
        - Faktor internal

        Missing:
        - Tidak ada

        Keputusan:
        ADVANCE

        ----------------------

        CONTOH 2:

        Pertanyaan:
        pola ini familiar ga buat kamu?

        Jawaban user:
        "iya familiar banget, dulu pas SMA juga gini, terus pas ospek juga, pas ngerjain tugas besar juga. kayaknya emang selalu gini deh tiap ada hal penting"

        Konteks sejauh ini:
        - overthinking di situasi penting

        Analisis:
        - Pola: Ada → terjadi berulang di berbagai konteks (SMA, ospek, tugas besar)
        - Faktor internal: Tidak ada → belum ada penjelasan kenapa pola ini terjadi

        Fulfilled:
        - Pola

        Missing:
        - Faktor internal

        Keputusan:
        STAY

        ----------------------

        CONTOH 3:

        Pertanyaan:
        kenapa menurut kamu pola ini sering terjadi?

        Jawaban user:
        "mungkin aku emang orangnya gampang overthinking sih, jadi tiap ada hal penting langsung kepikiran macem-macem"

        Konteks sejauh ini:
        - sering overthinking di situasi penting

        Analisis:
        - Pola: Ada → terjadi berulang di situasi penting
        - Faktor internal: Tidak ada → "aku orangnya overthinking" hanya label diri, belum menjelaskan penyebab yang mendasari

        Fulfilled:
        - Pola

        Missing:
        - Faktor internal

        Keputusan:
        STAY
        """

    if stage == "reasoning":
        return f"""
        Fokus: Penyebab → insight bermakna

        Target: {target_stage}

        ELEMEN YANG HARUS DICARI:
        1. Insight: pemahaman baru yang lebih dalam tentang diri sendiri (ditandai dengan kejelasan, bukan sekadar dugaan)
        2. Perubahan cara pandang: adanya pergeseran perspektif (misalnya dari A → ternyata B)
        3. Dampak: konsekuensi atau pengaruh pola tersebut terhadap pikiran, emosi, atau perilaku

        CARA MENILAI (WAJIB IKUTI URUTAN INI):
        1. Dari konteks + jawaban, identifikasi elemen yang SUDAH ada → masukkan ke fulfilled
        2. Identifikasi elemen yang BELUM ada → masukkan ke missing
        3. Jangan hanya melihat jawaban terakhir, gunakan konteks untuk melihat akumulasi
        4. Satu kalimat bisa memenuhi lebih dari satu elemen

        ELEMEN FULFILLED KETIKA:
        - Insight : Insight jelas (bukan dugaan, tidak menggunakan "mungkin", "kayaknya")
        - Perubahan cara pandang : Ada pergeseran cara pandang yang spesifik
        - Dampak : User mampu menjelaskan dampak dari pola terhadap dirinya

        ELEMEN MISSING KETIKA:
        - Insight : Insight masih umum atau generik (tidak spesifik ke diri sendiri)
        - Perubahan cara pandang : Masih memiliki cara pandang yang sama 
        - Dampak : Belum ada penjelasan dampak

        ADVANCE hanya jika:
        -Ketiga elemen fulfilled

        STAY jika:
        -Salah satu elemen missing
        ----------------------

        CONTOH 1:

        Pertanyaan:
        menurut kamu, kenapa pola ini terus muncul?

        Jawaban user:
        "ternyata aku takut dilihat gagal sama orang lain, bukan takut gagalnya sendiri"

        Konteks sejauh ini:
        - sering takut gagal di situasi penting

        Analisis:
        - Insight: Ada → "ternyata" menunjukkan pemahaman baru yang spesifik
        - Perubahan cara pandang: Ada → dari takut gagal → takut dinilai orang
        - Dampak: Ada (implisit) → mempengaruhi cara melihat kegagalan

        Fulfilled:
        - Insight
        - Perubahan cara pandang
        - Dampak (implisit)

        Missing:
        - Tidak ada

        Keputusan:
        ADVANCE

        ----------------------

        CONTOH 2:

        Pertanyaan:
        apa yang paling ngaruh ke pola ini?

        Jawaban user:
        "mungkin karena dari kecil aku selalu dituntut sempurna sama orang tua. terus di sekolah juga selalu jadi yang terdepan. jadi kayaknya udah biasa dituntut. mungkin itu yang bikin aku kayak gini sekarang"

        Konteks sejauh ini:
        - pola perfeksionisme
        - tekanan dari masa kecil

        Analisis:
        - Insight: Tidak ada → masih berupa dugaan ("mungkin", "kayaknya")
        - Perubahan cara pandang: Tidak ada → belum ada pergeseran perspektif yang jelas
        - Dampak: Tidak ada → belum dijelaskan pengaruhnya ke diri saat ini

        Fulfilled:
        - 

        Missing:
        - Insight yang jelas
        - Perubahan cara pandang
        - Dampak

        Keputusan:
        STAY

        CONTOH 3:

        Pertanyaan:
        menurut kamu, kenapa kamu jadi sering nunda?

        Jawaban user:
        "aku sadar aku nunda itu bukan karena malas, tapi karena takut hasilnya ga sesuai ekspektasiku sendiri"

        Konteks sejauh ini:
        - sering menunda tugas
        - merasa tertekan dengan hasil

        Analisis:
        - Insight: Ada → "aku sadar" menunjukkan pemahaman baru yang spesifik
        - Perubahan cara pandang: Ada → dari "malas" → ternyata "takut ekspektasi sendiri"
        - Dampak: Ada → mempengaruhi perilaku menunda

        Fulfilled:
        - Insight
        - Perubahan cara pandang
        - Dampak

        Missing:
        - Tidak ada

        Keputusan:
        ADVANCE
        """

    if stage == "reconstructing":
        return """
        Fokus: Insight → aksi konkret

        Target: COMPLETED

        ELEMEN YANG HARUS DICARI:
        1. Tindakan spesifik: aksi yang jelas dan dapat dilakukan (bukan niat umum)
        2. Konteks: kapan, di situasi apa, atau bagaimana tindakan dilakukan
        3. Alasan: penjelasan kenapa tindakan ini relevan atau bisa membantu (berdasarkan insight sebelumnya)

        CARA MENILAI (WAJIB IKUTI URUTAN INI):
        1. Dari konteks + jawaban, identifikasi elemen yang SUDAH ada → masukkan ke fulfilled
        2. Identifikasi elemen yang BELUM ada → masukkan ke missing
        3. Jangan hanya melihat jawaban terakhir, gunakan konteks untuk melihat akumulasi
        4. Satu kalimat bisa memenuhi lebih dari satu elemen

        ELEMEN FULFILLED KETIKA:
        - Tindakan spesifik: aksi jelas dan operasional (bisa langsung dilakukan)
        - Konteks: ada penjelasan kapan atau bagaimana tindakan dilakukan
        - Alasan: ada hubungan jelas antara tindakan dan insight sebelumnya

        ELEMEN DIANGGAP MISSING KETIKA:
        - Tindakan spesifik: masih berupa niat umum atau abstrak (misal: "lebih baik", "lebih prepare")
        - Konteks: tidak ada penjelasan kapan atau bagaimana dilakukan
        - Alasan: tidak ada penjelasan kenapa tindakan ini akan membantu

        ADVANCE hanya jika:
        -Ketiga elemen fulfilled

        STAY jika:
        -Salah satu elemen missing

        ----------------------

        CONTOH 1 (pendek, ADVANCE):

        Pertanyaan:
        konkretnya, apa yang mau kamu coba lakuin beda?

        Jawaban user:
        "aku mau coba ingetin diri sendiri sebelum presentasi: yang penting aku udah prepare, bukan hasilnya. karena aku sadar anxiety-ku datang dari fokus ke hasil, bukan proses"

        Konteks sejauh ini:
        - anxiety dari fokus ke hasil
        - insight tentang pentingnya proses

        Analisis:
        - Tindakan spesifik: Ada → mengingatkan diri sebelum presentasi
        - Konteks: Ada → sebelum presentasi
        - Alasan: Ada → karena anxiety berasal dari fokus ke hasil

        Fulfilled:
        - Tindakan spesifik
        - Konteks
        - Alasan

        Missing:
        - Tidak ada

        Keputusan:
        ADVANCE

        ----------------------

        CONTOH 2 (panjang, STAY):

        Pertanyaan:
        kalau ada situasi serupa, mau respon gimana yang berbeda?

        Jawaban user:
        "aku mau lebih santai sih ke depannya. udah capek juga overthinking mulu. pengen bisa nikmatin prosesnya aja tanpa terlalu mikirin hasilnya. pokoknya mau coba lebih positive thinking deh dan ga terlalu keras sama diri sendiri"

        Konteks sejauh ini:
        - ingin berubah
        - merasa capek overthinking

        Analisis:
        - Tindakan spesifik: Tidak ada → masih berupa niat umum
        - Konteks: Tidak ada → tidak jelas kapan atau bagaimana dilakukan
        - Alasan: Tidak ada → tidak ada hubungan jelas dengan insight sebelumnya

        Fulfilled:
        - Niat untuk berubah

        Missing:
        - Tindakan spesifik
        - Konteks
        - Alasan

        Keputusan:
        STAY

        ----------------------

        CONTOH 3 (borderline, STAY):

        Pertanyaan:
        apa langkah konkret yang mau kamu ambil?

        Jawaban user:
        "kayaknya aku bakal coba lebih prepare sih sebelum presentasi biar ga terlalu panik"

        Konteks sejauh ini:
        - sering panik saat presentasi
        - ada insight tentang kurang persiapan

        Analisis:
        - Tindakan spesifik: Tidak jelas → "lebih prepare" masih terlalu umum (tidak operasional)
        - Konteks: Ada → sebelum presentasi
        - Alasan: Ada → untuk mengurangi panik

        Fulfilled:
        - Konteks
        - Alasan

        Missing:
        - Tindakan spesifik (apa bentuk prepare yang dimaksud)

        Keputusan:
        STAY
        """

    return ""


def get_judge_chain(stage, llm_judge):
    from langchain_core.messages import SystemMessage, HumanMessage
    from langchain_core.prompts import HumanMessagePromptTemplate, ChatPromptTemplate

    target_stage = NEXT.get(stage, "completed")
    stage_instr = judge_stage_instruction(stage, target_stage)

    # Build system message sebagai plain string dulu
    system_content = f"""
Kamu adalah evaluator refleksi berbasis framework 5R yang ketat.

Tahap saat ini: {stage}
Tahap target: {target_stage}

Tugas:
Tentukan apakah user BENAR-BENAR sudah memenuhi indikator tahap saat ini
sebelum boleh maju ke tahap berikutnya.

{stage_instr}

ATURAN PENTING:
- Jangan mudah ADVANCE — refleksi yang dangkal merugikan user
- Jawaban singkat (1-5 kata) hampir selalu STAY
- Sinyal implisit boleh ditangkap, tapi harus jelas
- Jika ragu → pilih STAY

Output wajib JSON murni tanpa tambahan apapun:
{{"verdict": "ADVANCE atau STAY", "fulfilled": [], "missing": []}}
"""

    prompt = ChatPromptTemplate.from_messages([
        SystemMessage(content=system_content),
        HumanMessagePromptTemplate.from_template("""
Percakapan terakhir:

{text}

Keputusan:
""")
    ])

    return prompt | llm_judge
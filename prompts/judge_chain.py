from llm.model import llm_judge
from langchain_core.prompts import ChatPromptTemplate
from fsm.states import NEXT

def judge_stage_instruction(stage, target_stage):

    if stage == "reporting_responding":
        return f"""
        Fokus:
        - Bedakan antara deskripsi/emosi vs pola diri

        Target: {target_stage}

        ADVANCE jika:
        - User menyebut sifat/kecenderungan diri (perfeksionis, overthinking, dll)
        - Ada generalisasi (kayaknya aku, sering sih, biasanya)
        - Ada pola implisit meskipun singkat

        STAY jika:
        - Hanya cerita kejadian
        - Hanya emosi tanpa refleksi diri
        """

    if stage == "relating":
        return f"""
        Fokus:
        - Bedakan antara pola vs penyebab

        Target: {target_stage}

        ADVANCE jika:
        - User mulai menjelaskan "kenapa"
        - Ada hipotesis penyebab (meskipun belum yakin)
        - Menyebut faktor internal (takut gagal, tekanan, dll)

        STAY jika:
        - Hanya menyebut pola tanpa penjelasan
        """

    if stage == "reasoning":
        return f"""
        Fokus:
        - Bedakan antara hipotesis vs insight

        Target: {target_stage}

        ADVANCE jika:
        - Ada insight baru (aku mulai sadar…, ternyata…)
        - Ada perubahan cara pandang
        - User menyadari dampak dari pola pikirnya

        STAY jika:
        - Hanya menebak penyebab tanpa insight
        """

    if stage == "reconstructing":
        return f"""
        Fokus:
        - Bedakan antara insight vs aksi

        Target: COMPLETED

        ADVANCE jika:
        - Ada tindakan konkret
        - Ada langkah spesifik (misalnya: "aku akan mulai...")
        - Realistis dan bisa dilakukan

        STAY jika:
        - Masih berupa insight
        - Masih abstrak (harus lebih baik, pengen berubah)
        """

    return ""

def get_judge_chain(stage, llm_judge):

    target_stage = NEXT.get(stage, "completed")
    stage_instruction = judge_stage_instruction(stage, target_stage)

    prompt = ChatPromptTemplate.from_messages([
        (
            "system",
            f"""
            Kamu adalah evaluator refleksi berbasis framework 5R.

            Tahap saat ini: {stage}
            Tahap target: {target_stage}

            Tugasmu:
            Menentukan apakah respons user menunjukkan PERGERAKAN
            dari tahap saat ini menuju tahap target.

            {stage_instruction}

            ATURAN PENTING:
            - Gunakan interpretasi semantik, bukan literal
            - Tangkap sinyal implisit (tidak harus eksplisit)
            - Jangan menunggu jawaban sempurna
            - Lebih baik ADVANCE sedikit lebih cepat daripada terlalu lambat

            CONTOH SINYAL IMPLISIT:
            - "aku perfeksionis" → pola
            - "aku takut gagal" → penyebab
            - "kayaknya aku emang gini" → refleksi diri
            - "what if..." → reasoning awal

            ATURAN KEPUTUSAN:
            - ADVANCE jika ADA indikasi menuju tahap target
            - STAY jika TIDAK ADA indikasi sama sekali

            OUTPUT:
            Hanya satu kata:
            ADVANCE atau STAY
            """
        ),
        (
            "human",
            """
            Pertanyaan sebelumnya:
            {question}

            Respons user:
            {text}

            Keputusan:
            """
        )
    ])

    return prompt | llm_judge
from llm.model import llm_judge
from langchain_core.prompts import ChatPromptTemplate
from fsm.states import NEXT


def judge_stage_instruction(stage, target_stage):

    if stage == "reporting_responding":
        return f"""
    Fokus:
    - Bedakan antara deskripsi/emosi vs refleksi diri

    Target: {target_stage}

    ADVANCE jika ada minimal satu:
    - Self-assessment (aku merasa..., aku rasa..., aku kayaknya...)
    - Sifat/kecenderungan diri (perfeksionis, overthinking, dewasa, siap)
    - Perubahan kondisi (akhir-akhir ini, sekarang, belakangan ini)
    - Generalisasi ringan (biasanya, sering, kayaknya aku)

    STAY jika:
    - Hanya cerita kejadian
    - Hanya emosi tanpa refleksi diri
    """

    if stage == "relating":
        return f"""
        Fokus:
        - Pola → penyebab

        Target: {target_stage}

        ADVANCE jika ada:
        - Penjelasan "kenapa"
        - Hipotesis penyebab (mungkin karena...)
        - Faktor internal (takut gagal, tekanan, dll)

        STAY jika:
        - Hanya menyebut pola tanpa sebab
        """

    if stage == "reasoning":
        return f"""
        Fokus:
        - Penyebab → insight

        Target: {target_stage}

        ADVANCE jika ada:
        - Insight (aku mulai sadar…, ternyata…)
        - Perubahan cara pandang
        - Pemahaman dampak dari pola

        STAY jika:
        - Masih hipotesis tanpa insight
        """

    if stage == "reconstructing":
        return """
        Fokus:
        - Insight → aksi

        Target: COMPLETED

        ADVANCE jika:
        - Ada tindakan konkret
        - Ada langkah spesifik (aku akan mulai...)
        - Realistis

        STAY jika:
        - Masih insight / niat umum
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

                Tugas:
                Menentukan apakah respons user menunjukkan PERGERAKAN ke tahap berikutnya.

                {stage_instruction}

                ATURAN:
                - Gunakan interpretasi semantik
                - Tangkap sinyal implisit
                - Jangan tunggu jawaban sempurna
                - Cukup satu sinyal → ADVANCE
                - Jangan lompat lebih dari satu tahap

                Jika ragu → pilih ADVANCE

                OUTPUT:
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
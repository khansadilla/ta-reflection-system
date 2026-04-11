from llm.model import llm_judge
from langchain_core.prompts import ChatPromptTemplate
from fsm.states import NEXT


def judge_stage_instruction(stage, target_stage):

    if stage == "reporting_responding":
        return f"""
        Fokus: Deskripsi/emosi → refleksi diri

        Target: {target_stage}

        ADVANCE hanya jika user menunjukkan SEMUA ini:
        - Sudah menceritakan apa yang terjadi (konteks jelas)
        - Sudah mengekspresikan perasaan/reaksi personal
        - Ada minimal satu sinyal refleksi diri:
          (aku merasa..., aku kayaknya..., aku sering...)

        STAY jika:
        - Konteks kejadian masih samar
        - Hanya emosi tanpa refleksi diri
        - Jawaban terlalu singkat (1-3 kata)
        """

    if stage == "relating":
        return f"""
        Fokus: Pola → penyebab

        Target: {target_stage}

        ADVANCE hanya jika:
        - User sudah menghubungkan pengalaman dengan pola diri
        - Ada penjelasan "kenapa" yang jelas
        - Ada faktor internal yang disebutkan (takut gagal, tidak percaya diri, dll)

        STAY jika:
        - Hanya menyebut pola tanpa sebab ("iya sering terjadi")
        - Penyebab masih samar atau eksternal saja
        - Belum ada koneksi ke diri sendiri
        """

    if stage == "reasoning":
        return f"""
        Fokus: Penyebab → insight bermakna

        Target: {target_stage}

        ADVANCE jika ada SALAH SATU:
        - Ada insight eksplisit (aku sadar..., ternyata..., aku baru nyadar...)
        - Ada perubahan cara pandang yang jelas
        - User bisa menjelaskan DAMPAK dari pola yang ditemukan

        STAY jika:
        - Masih hipotesis tanpa insight (mungkin karena...)
        - Insight terlalu dangkal atau generik
        - Belum ada pemahaman dampak
        """

    if stage == "reconstructing":
        return """
        Fokus: Insight → aksi KONKRET

        Target: COMPLETED

        ADVANCE hanya jika user menyebutkan:
        - Tindakan spesifik yang akan dilakukan (bukan niat umum)
        - Ada konteks kapan/bagaimana akan dilakukan
        - Ada alasan kenapa itu akan berhasil

        STAY jika:
        - Masih niat umum ("aku mau lebih baik", "aku akan coba")
        - Tidak ada langkah konkret
        - Tidak ada argumen kenapa rencana itu akan works
        """

    return ""


def get_judge_chain(stage, llm_judge):

    target_stage = NEXT.get(stage, "completed")
    stage_instr = judge_stage_instruction(stage, target_stage)

    prompt = ChatPromptTemplate.from_messages([
        (
            "system",
            f"""
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

            OUTPUT:
            Hanya tulis ADVANCE atau STAY, tanpa penjelasan.
            """
        ),
        (
            "human",
            """
            Percakapan terakhir:

            {text}

            Keputusan:
            """
        )
    ])

    return prompt | llm_judge
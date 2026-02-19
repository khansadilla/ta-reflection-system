# Round 2.3 — Upgrade Mekanisme Transisi 5R (LLM-as-Judge)

## Tujuan
Mengganti mekanisme transisi antar tahap 5R (Reporting_Responding, Relating, Reasoning, Reconstructing) dari rule-based heuristik menjadi LLM-as-Judge berbasis rubric eksplisit, untuk meningkatkan evaluasi semantik terhadap kedalaman refleksi tanpa kehilangan kontrol struktural.

## Hipotesis
Jika seluruh transisi antar tahap 5R dievaluasi menggunakan LLM-as-Judge dengan rubric operasional yang jelas, maka:

- Evaluasi kedalaman refleksi menjadi lebih fleksibel terhadap variasi bahasa alami pengguna.
- Transisi antar tahap tidak terlalu bergantung pada keyword literal.
- Sistem tetap menjaga struktur progresif 5R tanpa lompatan prematur.
- Kedalaman refleksi meningkat secara bertahap dan lebih konsisten.

## Masalah yang Diamati (pada Rule-Based)
- Evaluasi terlalu bergantung pada pencocokan marker eksplisit.
- Respons natural dan singkat yang secara makna cukup mendalam dapat gagal lolos.
- Sistem tidak mampu menangkap makna implisit secara fleksibel.
- Decision boundary terlalu literal dan sensitif terhadap variasi wording.

## Intervensi

- Menghapus seluruh rule-based gating berbasis keyword.
- Mengganti mekanisme transisi dengan LLM-as-Judge untuk setiap tahap.
- Menyediakan rubric eksplisit untuk masing-masing tahap 5R.
- LLM diminta memberikan keputusan biner: `ADVANCE` atau `STAY`.

### Rubric Operasional per Tahap

#### Reporting_Responding
**Advance jika:**
- Respons menyebutkan konteks spesifik (siapa, apa, atau di mana).
- Respons mengandung reaksi personal berupa emosi atau pikiran.

**Stay jika:**
- Deskripsi terlalu umum.
- Tidak ada reaksi personal.

---

#### Relating
**Advance jika:**
- Respons menghubungkan pengalaman dengan pengalaman masa lalu.
- Respons mengaitkan dengan nilai, kebiasaan, atau pola pribadi.

**Stay jika:**
- Hanya mengulang emosi tanpa membuat koneksi.
- Tidak ada hubungan dengan pengalaman lain.

---

#### Reasoning
**Advance jika:**
- Respons mengidentifikasi faktor penyebab yang signifikan.
- Respons memberikan penjelasan mengapa hal tersebut terjadi.

**Stay jika:**
- Hanya mendeskripsikan ulang kejadian.
- Hanya menyalahkan faktor luar tanpa analisis.

---

#### Reconstructing
**Advance jika:**
- Respons menyusun rencana tindakan yang konkret dan spesifik.

**Stay jika:**
- Rencana terlalu abstrak atau berupa harapan umum.
- Tidak ada tindakan yang dapat diobservasi.

## Evaluasi Awal

### Clean / Controlled Test Cases
- Mayoritas kasus diklasifikasikan sesuai ekspektasi.
- Transisi antar tahap tidak terjadi secara prematur.
- Decision relatif konsisten untuk respons eksplisit.

### Realistic / Messy Test Cases
- Sistem cenderung konservatif (lebih memilih STAY pada kasus ambigu).
- Respons pendek dan implisit kadang tertahan meskipun secara manusia cukup reflektif.
- Tidak ditemukan perilaku loncatan tahap tanpa grounding.

## Insight

- LLM-as-Judge meningkatkan fleksibilitas semantik dibanding rule-based.
- Decision boundary menjadi lebih adaptif, namun tidak sepenuhnya deterministik.
- Sistem lebih stabil ketika dirancang konservatif dibanding terlalu permisif.
- Framing prompt sangat memengaruhi stabilitas evaluasi.

## Kesimpulan Round 2.3

Upgrade ke LLM-as-Judge pada seluruh tahap 5R:

- Mengurangi ketergantungan pada keyword literal.
- Menjaga struktur progresif refleksi secara eksplisit.
- Meningkatkan adaptivitas terhadap bahasa natural pengguna.
- Cukup stabil untuk dilanjutkan ke iterasi berikutnya (RAG dan kalibrasi prompt lanjutan).

Mekanisme ini dibekukan sebagai baseline sebelum integrasi komponen lain.


# Round 2.1 — Penyempurnaan Gating Reasoning

## Kondisi Awal (Baseline)
Transisi antar stage hanya berdasarkan panjang teks (>20 karakter).
Tidak ada validasi khusus sesuai stage.

## Masalah yang Ditemukan
- Reasoning sering terlalu dangkal.
- Transisi ke Reconstructing terjadi terlalu cepat.
- Insight terasa belum “earned”.
- Gating berbasis panjang teks tidak cukup menjamin adanya refleksi kausal.

## Intervensi Desain
Menambahkan gating khusus untuk stage Reasoning.

Aturan baru:
Jawaban harus mengandung marker kausal eksplisit
(contoh: "karena aku", "aku jadi").

Jika tidak mengandung marker → tetap di stage Reasoning.

## Implementasi
- Memodifikasi fungsi gate().
- Menambahkan daftar reasoning_markers.
- Menambahkan pengecekan khusus saat stage == "reasoning".

## Observasi

### Dampak Positif:
- Reasoning terasa lebih dalam.
- Struktur kausal lebih jelas.
- Refleksi lebih grounded.

### Keterbatasan:
- Marker terlalu sempit.
- Beberapa reasoning valid tidak lolos karena tidak memakai kata “karena” atau “jadi”.
- Rule sensitif terhadap variasi bahasa.

## Keputusan
Versi ini dibekukan sebagai eksperimen terkontrol.

Pengembangan lanjutan:
- Memperluas daftar marker
- Mengganti rule-based dengan evaluasi semantik berbasis LLM (di round berikutnya)

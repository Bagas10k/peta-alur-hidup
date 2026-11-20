# Model peta, format v2

Objek JSON UTF-8. `title` ringkas dan spesifik; `steps` daftar aksi, `edges` daftar panah terarah, `unknowns` daftar batas atau pertanyaan. Satu entri `steps` memiliki `id` huruf ASCII diikuti huruf/angka/underscore, `label`, `actor`, `before`, `after`, `evidence` (path sumber relatif dengan nomor baris 1-based), dan `tables` (objek nama tabel → operasi dipisah koma: `create,read,update,delete`). Jangan memasukkan isi kode, nama pelanggan, token atau data contoh operasional. Tulis `Belum terverifikasi` untuk fakta yang tidak terbukti. Pakai `{}` bila tidak ada akses data yang dapat dicantumkan; jelaskan di `unknowns` bila pembaca tidak dapat menelusurinya. State per entitas; `before` juga boleh memuat guard/izin, `after` memuat efek kondisional. Tambahkan lokasi bukti pendukung dalam catatan bila policy/event terpisah. Setiap panah `{ "from": "ID", "to": "ID", "label": "syarat atau urutan" }`. Cabang alternatif berasal dari status yang sama, bukan dari hasil cabang yang bertentangan.

```json
{"title":"Proses dokumen","steps":[{"id":"S1","label":"Baca dokumen","actor":"CLI","before":"File tersedia","after":"Konten terbaca","evidence":"app.py:1","tables":{}}],"edges":[],"unknowns":["Contoh sintetis; sesuaikan bukti dengan source proyek."]}
```

`--check` membandingkan keluaran dengan model dan memeriksa lokasi sumber; itu bukan pembuktian bahwa seluruh narasi benar atau semua fungsi telah terpetakan. Agen wajib membaca ulang bukti, terutama kondisi negatif, event asinkron dan operasi yang disembunyikan ORM. Artefak GitHub adalah Markdown dengan diagram Mermaid serta tabel teks yang tetap terbaca tanpa perender diagram.

---
name: peta-alur-hidup
description: "Use when mapping projects. Trace workflows from source."
version: 2.0.0
author: Bagas Saputra & Hermes Agent
license: MIT
platforms: [windows, linux, macos]
metadata:
  hermes:
    tags: [workflow, living-documentation, static-analysis]
---

# Peta Alur Hidup

Jika pengguna mengetik `peta-alur-hidup` atau `/peta-alur-hidup` tanpa argumen, itu permintaan untuk **langsung memetakan proyek aktif dan menyimpan hasilnya**, bukan untuk menampilkan bantuan. Jangan minta nama modul jika folder proyek sudah jelas. Argumen bebas seperti `retur barang` mempersempit fokus. `cek` berarti periksa hasil sebelumnya tanpa menulis. Hormati arahan eksplisit baca-saja atau lokasi keluaran pengguna.

## Jalur satu panggilan

1. Tetapkan ROOT dari workspace sesi atau path yang disebut, bukan direktori instalasi skill atau cache terminal. Jangan memindai home, seluruh drive, direktori induk berisi proyek-proyek tak terkait, atau repo lain. Jika tidak ada workspace/path yang bisa dikenali, baru minta path. Baca aturan lokal. Jika repo telah memiliki generator peta kanonis yang dikenal, pertahankan fiturnya (misalnya pemeriksaan transisi, dampak Git, jurnal). Inspeksi sumber command dahulu; gunakan jalur dokumentasi lokal yang terverifikasi aman. Jangan menimpa peta khusus proyek dengan versi generik.
2. Temukan lokasi skill dari `skill_view` (SKILL). Gunakan Python 3.12+ dan panggil skrip dengan path absolut, dalam argumen terpisah atau kutip path berspasi. Jalankan `python "SKILL/scripts/discover.py" "ROOT"`. Hasilnya inventaris nama, **bukan** hasil analisis. Periksa manifest dan entry point dengan alat baca. Jangan menginstal dependensi aplikasi, menjalankan kode dari repo yang dianalisis, membaca `.env`, dump, kredensial, atau mengambil data operasional. Helper membaca lokal; model Hermes tetap mengikuti konfigurasi provider pengguna.
3. Kelompokkan modul yang terlihat, identifikasi pemicu pengguna/API/job/event, dan telusuri alur utama yang dapat dibuktikan dari awal ke akhir, termasuk cabang gagal/tolak bila ada. Gunakan rute → handler → aturan akses/syarat → write/efek → penerus. Untuk pustaka/CLI gunakan input → validasi → proses → hasil, tanpa mengarang tabel. Bedakan aktor yang diotorisasi server dari dugaan atas nama menu. Jangan artikan urutan definisi fungsi sebagai urutan eksekusi. Titik tunggal sah jika hanya itu yang terbukti; jangan menciptakan panah demi grafik. Jika tidak ada bukti aksi (mis. repo aset), jelaskan tanpa membuat peta fiktif.
4. Buat model dan laporan per proyek, default `docs/peta-alur-hidup/model.json` dan `docs/peta-alur-hidup/ALUR.md`. Model mengikuti [references/model.md](references/model.md). Untuk monorepo besar, mulai dari alur dominan lalu petakan alur independen tanpa menghubungkannya secara palsu. Sebutkan modul terpetakan, yang belum, dan batas scan di `unknowns`; jangan diam-diam menyebut sampel sebagai seluruh proyek. Boleh bagi per modul dalam subfolder dan buat indeks ringkas bila perlu. Jika model sudah ada, baca dan gabungkan perubahan yang terverifikasi; jangan menimpa catatan manual atau file asing. Tidak perlu menambah item menu, migrasi, atau CI pada repo target.
5. Dari ROOT jalankan `python "SKILL/scripts/render.py" docs/peta-alur-hidup/model.json --root . --output docs/peta-alur-hidup/ALUR.md`, lalu ulangi dengan `--check`. Gunakan pasangan path yang sesuai jika per modul. Tinjau grafik, tabel langkah, indeks operasi data, dan bagian belum diketahui. Periksa setiap panah terhadap guard dan identitas data, bukan cuma eksistensi ID. Untuk mode `cek`, jangan regenerate: jalankan `--check`, inventaris ulang, baca ulang handler dan guard terhadap klaim, laporkan perubahan termasuk aksi baru yang belum dipetakan. Jika pengguna meminta analisis perubahan, pakai diff lokal; jangan mengklaim seluruh perubahan runtime terdeteksi.
6. Laporkan path yang bisa dibuka, satu alur utama, cakupan, pemeriksaan yang dijalankan, dan batasan penting. Jika kurang bukti, tandai. Python/helper tidak tersedia? Lakukan inspeksi manual dan serahkan diagram Markdown + tabel dengan sumber; nyatakan bahwa pemeriksa otomatis tidak dijalankan. Tidak ada izin otomatis untuk commit, push, atau publish keluaran proyek.

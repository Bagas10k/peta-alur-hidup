# Peta Alur Hidup

Buka Hermes di folder proyek lalu ketik **`/peta-alur-hidup`**. Hermes menelusuri kode dan membuat peta alur, tabel langkah, indeks operasi database, dan daftar bagian yang belum bisa dibuktikan. Tidak perlu menjelaskan struktur proyek atau menyiapkan model sendiri. Skill ini mendokumentasikan workflow, bukan menjalankan transaksi atau mengubah aturan bisnis.

## Pasang sekali

Butuh Hermes Agent dengan akses baca/tulis workspace, terminal, dan Python 3.12+ (stdlib saja). Jalankan sekali di terminal:

```sh
hermes skills install Bagas10k/peta-alur-hidup/skills/peta-alur-hidup
```

Untuk instalasi dari hasil unduh/clone, salin **seluruh folder** `skills/peta-alur-hidup` ke direktori `skills/` profil aktif; jangan salin `SKILL.md` saja. Jangan buat duplikat jika nama yang sama sudah terpasang. Mulai sesi Hermes baru di folder proyek tujuan.

## Terapkan di proyek sendiri

1. Buka terminal di akar proyek yang ingin dipetakan, lalu jalankan `hermes`. Skill terpasang di profil Hermes, bukan sebagai dependency proyek.
2. Ketik `/peta-alur-hidup`. Agen membaca kode, menelusuri alur yang bisa dibuktikan, lalu menyimpan dokumen; tidak perlu membuat model JSON secara manual.
3. Buka `docs/peta-alur-hidup/ALUR.md` di preview Markdown dengan dukungan Mermaid, misalnya di GitHub. Bila proyek sudah punya generator dokumentasi kanonis, lokasi aslinya dipertahankan.
4. Sesudah kode berubah, ketik `/peta-alur-hidup cek` untuk memeriksa tanpa menulis. Ketik `/peta-alur-hidup` kembali untuk memperbarui hasil berdasarkan analisis baru.

Pemakaian skill tidak mengubah transaksi, saldo, aturan bisnis, atau menu aplikasi. Model dan laporan adalah dokumen lokal; membagikannya tetap keputusan pengguna.

| Ketik di chat Hermes | Hasil |
|---|---|
| `/peta-alur-hidup` | Analisis workspace aktif dan buat peta |
| `/peta-alur-hidup retur barang` | Fokus satu modul |
| `/peta-alur-hidup cek` | Periksa peta dan sumber tanpa menulis |

Buka `docs/peta-alur-hidup/ALUR.md` dengan preview Markdown yang mendukung Mermaid. Tabel tetap terbaca sebagai teks. `model.json` di sebelahnya adalah sumber diagram. Untuk repo yang sudah mempunyai generator peta sendiri, skill mempertahankan format dan lokasi aslinya.

## Contoh & verifikasi lokal

[Contoh laporan pengajuan](examples/pengajuan/ALUR.md) memakai kode sintetis yang dapat diperiksa di [workflow.py](examples/pengajuan/workflow.py). Dari akar repo paket ini:

```sh
python skills/peta-alur-hidup/scripts/discover.py examples/pengajuan
python skills/peta-alur-hidup/scripts/render.py examples/pengajuan/model.json --root examples/pengajuan --output examples/pengajuan/ALUR.md --check
python -m unittest discover -s tests -v
```

Hermes yang membaca kode dan menentukan alur; `discover.py` menginventaris file dan `render.py` memvalidasi model serta menghasilkan laporan yang konsisten. Pemeriksaan otomatis bukan jaminan SOP benar atau seluruh cabang dinamis ditemukan. Skill tidak memerlukan koneksi database dan tidak mengunggah laporan ke GitHub. Bila memakai provider model jarak jauh, potongan kode yang dibaca agen dapat masuk ke konteks provider tersebut. Tinjau laporan sebelum membagikannya. Lisensi: MIT.

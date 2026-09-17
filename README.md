# GDT WORKS — portofolio one page

## Pembaruan: pesanan dan animasi fade-in

Lihat **PANDUAN-PESANAN.md** untuk fitur terbaru: panel desktop lokal `scripts/manage-orders.py`, judul nama pesanan, progres 0–100%, status pengiriman/diterima, dan slideshow 3–12 foto. Panel ini memperbarui berkas situs lokal; bukan admin online. Hosting tetap perlu diperbarui dengan mengunggah ulang `dist`. Petunjuk progres lama di bawah tetap merupakan format kompatibilitas, bukan format kartu pesanan baru. Tidak ada foto/pesanan nyata tambahan yang direkayasa.


## Struktur berkas

| Berkas | Peran |
| --- | --- |
| `dist/index.html` | Struktur semantik satu halaman dan metadata |
| `dist/styles.css` | Tema, layout, responsivitas, tampilan cetak, gerakan |
| `dist/script.js` | Interaksi browser, dialog, filter, menu, proses, kontak dan peta |
| `dist/content.js` | Konten publik hasil kompilasi; jangan diedit langsung |
| `dist/assets/hero.webp` | Konsep AI mecha full body untuk hero dan beberapa kartu |
| `dist/assets/mecha.webp` | Konsep AI detail mecha untuk galeri |
| `dist/assets/favicon.svg` | Ikon sederhana GDT |
| `dist/_headers` | Header keamanan untuk host yang mendukung format ini |
| `content/site.json` | Data editorial untuk diperbarui sebelum penerbitan |
| `scripts/prepare-content.py` | Validasi dan penyaringan konten yang disetujui |
| `scripts/verify.py` | Pemeriksaan sumber dan batas publikasi |
| `.openai/hosting.json` | Identitas Site yang sama dan direktori publik `dist` |
| `VERIFIKASI.md` | Hasil pemeriksaan dan batas validasi |

Website yang sudah disiapkan tidak membutuhkan instalasi npm, library JavaScript, font CDN, atau backend. Python 3 hanya dipakai pengelola untuk menyusun ulang konten dan menjalankan pemeriksaan lokal.


## Mengisi nomor, media sosial, alamat, dan peta

Pada objek `contact` di `content/site.json`:

| Properti | Nilai |
| --- | --- |
| `approved` | Boolean `true` setelah seluruh informasi kontak disetujui pemilik |
| `whatsapp` | Nomor resmi format internasional 8–15 digit; Indonesia diawali `62`, tanpa tanda plus, spasi, atau tanda hubung |
| `address` | Alamat workshop yang boleh dipublikasikan |
| `hours` | Hari dan jam operasional yang telah dikonfirmasi |
| `mapsUrl` | Tautan HTTPS resmi Google Maps, boleh kosong jika koordinat tersedia |
| `latitude`, `longitude` | Angka koordinat yang benar, atau keduanya `null` jika belum diketahui |

Domain peta yang diterima: `www.google.com`, `maps.google.com`, `maps.app.goo.gl`, pada HTTPS standar. URL dengan kredensial, domain menyerupai Google, atau port berbeda ditolak. Latitude harus -90 sampai 90 dan longitude -180 sampai 180. Jangan menggunakan koordinat acak sebagai isian sementara.

Nomor yang valid dan disetujui mengaktifkan WhatsApp otomatis. Memilih layanan atau tombol dalam dialog menyiapkan pesan konsultasi sesuai layanan. Website **tidak mengirim pesan otomatis**; pelanggan mengirimnya sendiri di WhatsApp.

Pada objek `socials`, isi URL profil Instagram dan toko Shopee resmi menggunakan HTTPS, lalu ubah `approved` menjadi `true`. Domain yang diterima adalah `instagram.com`, `www.instagram.com`, `shopee.co.id`, `www.shopee.co.id`, `shopee.id`, dan `www.shopee.id`. Menjalankan `prepare-content.py` akan membuat QR lokal di `dist/assets`, sehingga tombol dan QR tidak bergantung pada layanan QR eksternal. Jika URL atau nomor belum disetujui, kartu tetap tampil sebagai tempat yang siap diisi tanpa mengarah ke akun palsu.

Pembuatan ulang QR memerlukan paket Python `reportlab` hanya ketika salah satu kanal telah dikonfigurasi. QR yang sudah dihasilkan merupakan aset statis dan tidak memerlukan dependensi di browser.

Koordinat mengaktifkan tombol **Tampilkan peta**. Embed dimuat dari Google hanya setelah tombol ditekan. Tautan petunjuk arah tetap tersedia di luar embed. Jika hanya URL Google Maps tersedia, pengunjung dapat membuka petunjuk arah tanpa embed. Pengujian peta dan pengiriman WhatsApp yang sebenarnya menunggu data resmi.

## Mengganti konsep dengan hasil proyek nyata

Sunting setiap objek `projects` di `content/site.json`:

- `id`: unik, huruf kecil/angka/tanda hubung.
- `category`: `rakit`, `detailing`, `filet`, `repaint`, atau `repair`.
- `label`: nama layanan untuk tampilan dan pesan konsultasi.
- `title`, `subtitle`, `description`: teks faktual proyek.
- `image`: jalur aset lokal seperti `assets/nama-proyek.webp`.
- `alt`: deskripsi gambar yang akurat.
- `status`: status proyek yang sebenarnya.
- `focus`: keterangan teknis yang relevan.
- `result`: hasil pekerjaan yang memang dapat didukung dokumentasi.
- `concept`: `false` hanya jika entri merupakan pekerjaan nyata, bukan ilustrasi.
- `approved`: boolean `true` setelah izin publikasi diperoleh.

Setiap proyek yang belum disetujui dikeluarkan dari `dist/content.js`. Jika semua entri menjadi karya nyata, pemberitahuan galeri konsep disembunyikan otomatis. Jika keduanya bercampur, pemberitahuan menjelaskan adanya konsep dan karya; label masing-masing kartu tetap terlihat.

Untuk mengganti visual hero, ubah aset dan alt di `index.html`, serta label “VISUAL KONSEP AI” bila gambar penggantinya bukan konsep. Ilustrasi AI tidak boleh dipakai sebagai bukti pengerjaan pelanggan.

Optimalkan gambar menjadi WebP, sekitar 1600 px lebar dan sedapat mungkin di bawah 500 KB. Bersihkan metadata lokasi/EXIF, label pengiriman, wajah/identitas pihak lain, serta informasi sensitif dari foto sebelum publikasi.

## Menambah progres yang disetujui

Array `progress` awalnya kosong. Contoh **struktur untuk pengelola**, bukan data proyek nyata:

```json
{
  "id": "kode-proyek",
  "approved": false,
  "projectCode": "KODE-ANONIM",
  "title": "Judul proyek yang benar",
  "date": "2026-09-15",
  "stage": "Tahap pengerjaan yang benar",
  "description": "Penjelasan yang telah diperiksa pemilik.",
  "image": "assets/foto-proyek.webp",
  "alt": "Deskripsi foto sebenarnya",
  "timeline": [
    {
      "approved": false,
      "date": "2026-09-15",
      "stage": "Tahap pertama",
      "description": "Catatan publik yang benar."
    }
  ]
}
```

Tanggal contoh harus diganti dengan tanggal kegiatan sebenarnya. Gambar bersifat opsional untuk progres; jika `image` disediakan, asetnya harus tersedia dan `alt` wajib diisi. Rekaman induk dan setiap item timeline harus disetujui secara terpisah menggunakan boolean `true`. Catatan belum disetujui tidak dikirim ke browser. Rekaman diurutkan berdasarkan tanggal terbaru.

Gunakan kode anonim, bukan nama lengkap pelanggan, nomor telepon, alamat, atau nilai pesanan. `steps` adalah alur layanan umum dan selalu terdiri atas lima tahap, terpisah dari `progress`. Jika tahap pertama diubah, selaraskan juga fallback HTML di `#process-panel`.

## Batas publikasi dan keamanan

Penyaringan kini dilakukan **sebelum deploy**, bukan hanya menyembunyikan kartu dengan JavaScript:

1. `prepare-content.py` hanya memilih rekaman dengan `approved` boolean `true` dan hanya menyalin field publik yang dikenal.
2. Field tambahan seperti catatan internal atau data pelanggan tidak ikut dikompilasi.
3. Nomor, koordinat, tanggal, kategori, ID unik, dan jalur gambar divalidasi. Input tidak sesuai menghentikan persiapan, sehingga kesalahan dapat diperbaiki sebelum penerbitan.
4. Browser menulis data melalui `textContent` dan DOM API. Tidak ada `innerHTML`, `eval`, event handler inline, atau pemrosesan input sebagai kode.
5. Tidak ada database, login, unggahan, API aplikasi, analytics, cookie aplikasi, atau penyimpanan data pelanggan di browser.
6. CSP metadata membatasi script, stylesheet, font, serta gambar ke origin sendiri; melarang object, pengiriman form, base URL, dan koneksi API. Peta hanya diizinkan dari `https://www.google.com`.
7. `_headers` menyertakan CSP, `frame-ancestors`, `nosniff`, kebijakan referrer, pembatasan kamera/mikrofon/geolokasi/pembayaran, dan `X-Frame-Options`.
8. Tautan eksternal menggunakan `noopener noreferrer`; gerakan gambar hanya menerima nilai numerik yang dihitung dari pointer/scroll.


## Responsivitas dan aksesibilitas

- Breakpoint 1050 px, 760 px, dan 480 px mengatur navigasi, kolom, dan ukuran visual.
- Menu dapat ditutup dengan Escape, memilih tautan, atau klik di luar header.
- Dialog native mendukung Escape, klik latar, tombol tutup, dan pengembalian fokus.
- Filter memakai `aria-pressed` dan jumlah hasil diumumkan lewat live region.
- Tab proses mendukung panah atas/bawah, Home, dan End.
- Tautan lompat konten, fokus terlihat, alt, dan label kontrol disediakan.
- Reduced motion sistem menghentikan gerakan. Tombol Jeda gerakan memberi kontrol tambahan tanpa menyimpan preferensi.
- Isi utama dan accordion layanan tetap dapat dibaca tanpa JavaScript; galeri, detail, progres dinamis, kontak terkonfigurasi, dan embed memerlukan JavaScript.
- Gerakan hero memakai satu gambar dan CSS; tidak ada video otomatis atau mesin 3D berat.
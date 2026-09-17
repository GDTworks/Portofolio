# Verifikasi GDT WORKS — versi 2

Tanggal pemeriksaan: 15 September 2026. Desain diperbarui ke dominan hitam dengan aksen oranye; Site dan audiens pemilik dipertahankan.

## Hasil yang terverifikasi

Sembilan pengujian otomatis pada `scripts/verify.py` **lulus**:

1. Proyek, progres, dan kontak belum disetujui tidak masuk keluaran publik.
2. Field di luar daftar publik tidak bocor ke keluaran.
3. Persetujuan menerima boolean `true`, bukan string yang terlihat seperti true.
4. Progres publik dan timeline memerlukan persetujuan masing-masing.
5. Protokol berbahaya, domain peta palsu, URL berkredensial, port tidak sesuai, dan nomor tidak valid ditolak.
6. Koordinat di luar batas, string, boolean, atau pasangan tidak lengkap ditolak; koordinat nol yang valid diterima.
7. Jalur traversal, gambar eksternal, dan format aset yang tidak didukung ditolak.
8. Tanggal mustahil dan ID proyek duplikat ditolak.
9. Keluaran publik sama dengan hasil kompilasi sumber terkini.

Pemeriksaan statis **lulus** untuk sintaks kedua berkas JavaScript, keberadaan aset, ID unik, anchor internal, relasi ARIA, kait bagian WP-01–WP-09, blok CSS seimbang, breakpoint mobile, reduced motion, identitas direktori statis, serta tidak adanya PDF/data mahasiswa/berkas privat di keluaran publik.

Dua ilustrasi mecha diperiksa secara visual dan tersedia sebagai WebP lokal. Tidak ada dependensi runtime pihak ketiga. Peta eksternal hanya dibuat setelah aksi pengunjung bila koordinat resmi dikonfigurasi.

## Tinjauan pada kode

Menu mobile, filter, dialog, konteks konsultasi, renderer progres, tab proses, peta bersyarat, navigasi aktif, dan tombol jeda gerakan telah ditinjau pada sumber. Penggunaan `textContent` mencegah teks konten diinterpretasikan sebagai HTML. Header HTTP disediakan bersama CSP metadata.

## Keterbatasan

Tidak dijalankan browser otomatis, screenshot viewport, uji perangkat fisik, uji pembaca layar, uji penetrasi, atau verifikasi header respons produksi. Interaksi ditinjau pada kode, belum diuji melalui DOM browser. Pengiriman WhatsApp dan peta aktif belum dapat diuji karena nomor serta lokasi resmi belum tersedia.

WP-03/WP-04 masih memakai konsep, WP-05 belum memiliki progres aktual, dan WP-06/WP-07/WP-08 memerlukan data resmi untuk penggunaan pelanggan. Dokumen perencanaan tidak dianggap sebagai bukti bahwa foto, izin proyek tertentu, alamat, nomor, atau jam operasi telah diberikan.
# Pemeriksaan revisi pesanan — 15 September 2026

13 pengujian otomatis lulus, termasuk batas 0/100, penolakan nilai invalid, status pengiriman hanya sesudah 100%, minimal 3 dan maksimal 12 foto, penyaringan pesanan belum disetujui, dan kompatibilitas progres lama. Pemeriksaan statis HTML/ARIA/aset/CSS serta sintaks JavaScript lulus. Sintaks panel Python diperiksa dengan py_compile.

Panel desktop Tkinter dan interaksi browser belum diuji secara visual pada sesi ini. Uji tampilan HP/desktop, slide dengan tombol/keyboard/swipe, fade-in sekali, dan penyimpanan melalui panel pada komputer pengelola sebelum publikasi. Tidak ada pesanan/foto pelanggan nyata pada lampiran; bagian publik tetap kosong sampai pengelola mengisi dan menyetujui pesanan.

Catatan verifikasi versi sebelumnya di bawah adalah riwayat, bukan hasil uji fitur baru.

# GDT WORKS — pengelola pesanan & fade-in

Foto pesanan ditampilkan dalam rasio tetap **16:9** di desktop maupun HP, termasuk seluruh slide. Foto dengan rasio lain dipotong secara visual dari tengah tanpa diregangkan; berkas foto asli tidak diubah. Gunakan foto 16:9 (misalnya 1920 × 1080) agar seluruh komposisi terlihat. Tombol slide berada di luar area foto.

## Mengubah pesanan tanpa mengedit kode

1. Ekstrak ZIP ini di komputer. Gunakan Python 3 dengan Tkinter (antarmuka desktop).
2. Dari folder GDT-WORKS, jalankan `python scripts/manage-orders.py` (atau `python3`).
3. Klik **Pesanan baru**, atau pilih pesanan yang sudah ada.
4. Isi nama pesanan sebagai judul kartu, kode anonim, detail tahap, dan keterangan.
5. Geser persentase dari 0 sampai 100. Pilih **Proses pengerjaan**, **Proses pengiriman**, atau **Pesanan diterima**. Status pengiriman/diterima hanya diterima jika pengerjaan sudah 100%.
6. Pilih 3–12 foto JPG/PNG/WebP. Daftar mengikuti urutan slide; hapus foto pilihan lalu pilih penggantinya. Tombol kiri/kanan, keyboard, dan geser layar sentuh tersedia di situs. Slide tidak berpindah otomatis.
7. Periksa izin publikasi dan centang persetujuan. Klik **Simpan pesanan & perbarui situs lokal**.
8. Unggah ulang isi `dist` ke hosting yang digunakan. Pengunjung lalu dapat melihat data terbaru setelah memuat ulang halaman.

Panel ini lokal, bukan admin online atau server latar belakang. Tidak memerlukan login karena hanya berjalan pada komputer pengelola. Jangan mengunggah panel, `content`, atau `scripts` ke hosting publik. Jika Tkinter tidak tersedia, pasang komponen Tkinter untuk instalasi Python desktop Anda; alternatifnya edit `content/site.json` dan jalankan `python scripts/prepare-content.py`.

Belum ada data pesanan/foto asli pada lampiran, sehingga tidak dibuat klaim pesanan contoh di halaman publik. Buat pesanan pertama melalui panel untuk menampilkan kartu dan slideshow.

Persentase selalu menunjukkan **penyelesaian pengerjaan**, bukan persentase perjalanan kurir. Saat pengiriman, kartu tetap menampilkan 100% pengerjaan dengan label Proses pengiriman.

## Privasi dan cadangan

Gunakan nama pesanan yang boleh dipublikasikan, bukan nama lengkap pelanggan, alamat, atau nomor resi pribadi. Bersihkan EXIF dan informasi sensitif pada foto sebelum mengimpor. Foto yang diimpor berada di `dist/assets` dan publik. Foto lama tidak dihapus otomatis; membatalkan persetujuan menyembunyikan kartu tetapi tidak menghapus aset yang sebelumnya dipublikasikan. Hapus aset lama secara manual hanya setelah memastikan tidak digunakan oleh entri lain, lalu terbitkan ulang.

Panel mempertahankan data kontak, galeri, dan layanan lain. Versi sumber sebelum penyimpanan terakhir disalin ke `content/site.backup.json`. Cadangan tersebut hanya lokal dan jangan diunggah ke hosting. Bila sumber diubah program lain saat panel terbuka, panel menolak menimpanya; buka ulang panel terlebih dahulu.

## Animasi

Judul bagian, blok isi utama, kartu pesanan, dan kartu sosial menggunakan fade-in saat pertama kali masuk viewport. Pengamatan dihentikan setelah elemen muncul sehingga tidak berulang ketika scroll kembali. Mode reduced motion, jeda gerakan, cetak, dan JavaScript nonaktif tidak menyembunyikan isi.

## Pemeriksaan

Jalankan `python scripts/prepare-content.py` dan `python scripts/verify.py`. QR terkonfigurasi tetap membutuhkan ReportLab saat kompilasi, sesuai README versi sebelumnya.

## Revisi: hapus pesanan dan tata letak responsif

Pada layar lebar, setiap pesanan memakai satu kartu penuh dengan foto di kiri dan seluruh deskripsi, status, persentase, serta riwayat di kanan. Saat lebar area kartu 760 px atau kurang (atau layar 850 px atau kurang), deskripsi pindah ke atas dan foto ke bawah. Rasio foto tetap 16:9; tombol panah, keyboard, dan geser sentuh tetap tersedia.

### Menghapus pesanan
1. Jalankan `python scripts/manage-orders.py` dari folder GDT-WORKS.
2. Pilih pesanan yang ingin dihapus dari daftar atas.
3. Klik **Hapus pesanan**, periksa nama/kode pada dialog, lalu pilih **Ya**. Pilih **Tidak** untuk membatalkan.
4. Data sumber dan situs lokal langsung diperbarui. Tidak perlu menekan Simpan lagi. Jika pesanan terakhir dihapus, situs menampilkan kondisi belum ada pesanan.
5. Unggah ulang isi folder `dist` ke hosting. Muat ulang halaman; gunakan Ctrl+F5 jika tampilan lama masih tersimpan di browser.

Tombol hapus tidak aktif ketika membuat pesanan baru yang belum disimpan. Foto tidak ikut dihapus karena mungkin digunakan pesanan lain. Cadangan satu versi sebelum perubahan terakhir berada di `content/site.backup.json`; salin kembali menjadi `content/site.json` lalu jalankan `python scripts/prepare-content.py` untuk memulihkan. Tutup panel sebelum memulihkan cadangan. Penyimpanan/penghapusan berikutnya akan mengganti cadangan ini.

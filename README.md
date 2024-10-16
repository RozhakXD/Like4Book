# Like4Book
![Like4Book](https://github.com/user-attachments/assets/53dc8eec-61f8-4e41-8ba5-d4802099d5e7)

**Like4Book** adalah alat yang aman untuk menambah pengikut Facebook menggunakan layanan dari like4like.org. Alat ini memudahkan Anda menukarkan kredit dari Like4Like untuk mendapatkan pengikut di profil atau halaman Anda.

## Fitur Utama
- Tukarkan kredit dari Like4Like menjadi pengikut untuk profil atau halaman Facebook Anda dengan mudah.
- Jalankan misi follow Facebook untuk menambah kredit secara otomatis dan mempercepat proses mendapatkan pengikut.
- Kelola tautan Like4Like yang terhubung dengan akun Anda dengan praktis dan efisien.
- Antarmuka intuitif dengan sistem input terminal yang user-friendly, memudahkan navigasi dan penggunaan.
- Aman dan efisien, berjalan di latar belakang tanpa mengganggu aktivitas sehari-hari Anda.

## Persyaratan
- Python versi 3.x atau lebih baru.
- Module/Library:
    - `requests`
    - `rich`

## Instalasi
1. Clone repositori ini:
    ```bash
    git clone https://github.com/RozhakXD/Like4Book.git
    ```
2. Masuk ke direktori proyek:
    ```bash
    cd Like4Book
    ```
3. Instalasi dependencies:
    ```bash
    pip install -r requirements.txt
    ```
5. Jalankan aplikasi:
    ```bash
    python Run.py
    ```

## Troubleshooting
Jika Anda mengalami masalah saat menggunakan Like4Book, berikut adalah beberapa langkah yang dapat Anda lakukan untuk menyelesaikannya:
- **Masalah: Misi Follow Tidak Berjalan**
    - **Penyebab**: Delay mungkin terlalu pendek atau ada masalah dengan cookies akun Facebook.
    - **Solusi**: Coba perbesar delay misi follow (disarankan lebih dari 60 detik). Jika tidak berhasil, periksa cookies Facebook Anda.
- **Masalah: Gagal Mengambil Kredit dari Like4Like**
    - **Penyebab**: Cookies yang Anda gunakan mungkin kadaluarsa atau salah.
    - **Solusi**: Pastikan Anda memperbarui cookies dari akun Like4Like dan Facebook Anda. Periksa kembali file Cookie.json di folder Penyimpanan.
- **Masalah: Koneksi Gagal atau Waktu Tunggu Terlalu Lama**
    - **Penyebab**: Masalah koneksi internet atau server like4like.org sedang down.
    - **Solusi**: Pastikan koneksi internet Anda stabil dan coba lagi beberapa saat kemudian. Jika masalah terus berlanjut, coba periksa situs like4like.org untuk mengetahui status server.
- **Masalah: Credits Tidak Cukup**
    - **Penyebab**: Kredit yang dimiliki di like4like.org kurang dari jumlah minimal yang dibutuhkan.
    - **Solusi**: Pastikan Anda memiliki minimal 50 kredit di akun Like4Like sebelum menjalankan pertukaran pengikut.

## Peringatan (Warning)
- **Gunakan dengan Bijak**: Penggunaan **Like4Book** mungkin melanggar **Ketentuan Layanan** Facebook atau Like4Like. Anda bertanggung jawab penuh atas penggunaan alat ini.
- **Akun Bisa Terblokir**: Penggunaan yang berlebihan atau tidak wajar dapat menyebabkan akun Facebook atau Like4Like Anda diblokir. Gunakanlah fitur ini dengan hati-hati dan hindari penukaran pengikut secara besar-besaran dalam waktu singkat.

## Lisensi
Like4Book dirilis di bawah lisensi **MIT**. Anda bebas menggunakan, memodifikasi, dan mendistribusikan proyek ini dengan tetap menghormati ketentuan lisensi.

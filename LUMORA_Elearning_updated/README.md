# LUMORA — Website Mockup E-Learning

LUMORA adalah mockup website e-learning menggunakan Python Flask, HTML, dan CSS. Data akun, pertanyaan, dan diskusi disimpan secara lokal menggunakan SQLite.

## Fitur
- Login dan registrasi akun
- Profil pengguna
- Dashboard beranda
- Materi berdasarkan jenjang SD, SMP, SMA, dan Kuliah
- Halaman privat dengan kartu tutor (mockup)
- Tanya jawab: pengguna dapat menambahkan pertanyaan
- Diskusi: pengguna dapat membuat topik diskusi

## Cara menjalankan di VS Code (Windows)
1. Ekstrak ZIP ke folder yang mudah ditemukan.
2. Buka VS Code → **File → Open Folder** → pilih folder `LUMORA_Elearning`.
3. Pastikan Python sudah terpasang. Buka terminal VS Code (**Terminal → New Terminal**).
4. Buat virtual environment:
   ```powershell
   py -m venv .venv
   ```
5. Aktifkan:
   ```powershell
   .\.venv\Scripts\Activate.ps1
   ```
   Jika PowerShell memblokir aktivasi, gunakan Command Prompt dan jalankan:
   ```bat
   .venv\Scripts\activate.bat
   ```
6. Instal Flask:
   ```powershell
   pip install -r requirements.txt
   ```
7. Jalankan:
   ```powershell
   python app.py
   ```
8. Buka browser di **http://127.0.0.1:5000**

Saat pertama dijalankan, file database `lumora.db` dibuat otomatis. Buat akun lewat tombol **Daftar**.

## Catatan keamanan
Ini proyek mockup pembelajaran, bukan sistem produksi. Sebelum dipublikasikan, ganti `app.secret_key` dengan secret acak dari environment, nonaktifkan debug mode, tambahkan CSRF protection, pembatasan percobaan login, validasi lebih ketat, dan HTTPS.


Logo resmi LUMORA berada di `static/images/lumora-logo.png` dan digunakan pada navigasi website.

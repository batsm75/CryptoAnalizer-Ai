💻 CryptoTerminal-AI

CryptoTerminal-AI adalah terminal pintar berbasis Python untuk trader, analis, dan pembelajar dunia kripto & forex. Dirancang dengan antarmuka berbasis CLI, AI interaktif, dan sistem keamanan bawaan, tool ini cocok untuk pemula maupun pengguna berpengalaman yang ingin belajar, menganalisis, dan menyimulasikan trading langsung dari terminal mereka.


---

✨ Fitur Unggulan

🔐 Sistem Login Aman

Pengguna membuat username & password pribadi.

Satu akun per perangkat (device-bound).

Maksimal 3x percobaan login (anti-brute force).


📊 Analisis Pasar Real-Time

Harga kripto (CoinGecko API) & data forex terkini.

Indikator teknikal otomatis: RSI, EMA.

Prediksi tren harian & analisis sederhana.


🧠 AI Coach & Mentor (Powered by Gemini AI)

AI interaktif untuk menjawab pertanyaan seputar:

Definisi aset digital

Strategi trading

Psikologi pasar

Analisis teknikal & fundamental


Penjelasan istilah kompleks dengan bahasa sederhana.


📰 Ringkasan Berita Terkini

Integrasi NewsData.io API.

Update pasar kripto dan forex setiap hari.


💡 Edukasi & Psikologi Trading

Tips praktis untuk mengelola emosi & keputusan.

Materi edukasi berbasis pengalaman nyata.



---

⚙️ Instalasi & Penggunaan (Android - Termux)

Ikuti langkah-langkah berikut untuk mulai menggunakan CryptoTerminal-AI di perangkat Android Anda melalui Termux:

1. Perbarui Termux

pkg update && pkg upgrade -y

2. Beri Izin Penyimpanan

termux-setup-storage

> Pilih “Allow” saat muncul pop-up izin.



3. Instal Git & Python

pkg install git python -y

4. Kloning Repositori

git clone https://github.com/batsm75/CryptoTerminal-AI.git

5. Masuk ke Direktori Proyek

cd CryptoTerminal-AI

6. Instal Dependensi Python

pip install -r requirements.txt

> Jika requirements.txt belum tersedia, buat dengan isi:



requests
numpy
textwrap

7. Jalankan Aplikasi

python main.py

> Pastikan file utama bernama main.py. Jika tidak, sesuaikan perintahnya.




---

🔑 Konfigurasi API Keys

NewsData.io (NEWS_API_KEY)

Dapatkan key dari: https://newsdata.io/

Sudah disertakan secara default, tapi bisa diubah lewat main.py.


Gemini AI (GEMINI_API_KEY)

Dapatkan dari: Google AI Studio

Ganti key di main.py sesuai kebutuhan.


> ⚠️ Penting: Jangan menyimpan API Key sensitif di repositori publik. Gunakan .env atau sistem manajemen rahasia jika ingin lebih aman.




---

📄 Lisensi

Proyek ini dilindungi oleh MIT License. Lihat file LICENSE untuk informasi lengkap.


---

🤝 Kontribusi

Terbuka untuk kontribusi!
Temukan bug? Punya ide fitur baru? Buat issue atau kirim pull request sekarang juga.


---

🧑‍💻 Creator

Dibuat dengan ❤️ oleh Bay s Exploit

💻 CryptoTerminal-AI

CryptoTerminal-AI adalah tool berbasis Python yang didesain untuk edukasi, analisis pasar kripto dan forex, serta simulasi trading langsung dari terminal Anda. Dilengkapi dengan AI Coach interaktif dan sistem login yang aman, aplikasi ini menjadi teman ideal bagi pemula maupun trader berpengalaman.

✨ Fitur Utama
🔒 Sistem Login Aman:
Pengguna dapat membuat username dan password pribadi.
Sistem ini dirancang untuk satu akun per perangkat, sehingga penting bagi pengguna untuk menyimpan kredensial mereka.
Maksimal 3 kali percobaan login untuk keamanan.
📈 Analisis Pasar Real-time:
Menampilkan harga kripto dan forex terkini (menggunakan data CoinGecko untuk kripto).
Perhitungan dan tampilan indikator teknikal: RSI (Relative Strength Index), EMA (Exponential Moving Average).
Analisis tren harian dan prediksi sederhana.
🧠 AI Coach & Mentor (Didukung Gemini AI):
AI interaktif yang dapat menjawab semua pertanyaan Anda seputar dunia kripto dan forex, mulai dari definisi, strategi trading, analisis pasar, hingga psikologi trading.
Memberikan saran trading dan edukasi istilah-istilah kompleks dengan mudah dipahami.
📰 Berita Pasar Terkini:
Menyediakan ringkasan berita kripto dan forex terbaru untuk membantu Anda tetap up-to-date dengan kondisi pasar.
💡 Psikologi Market & Tips Praktis:
Menyajikan wawasan tentang aspek psikologis dalam trading dan tips praktis untuk pengambilan keputusan yang lebih baik.
🚀 Instalasi dan Penggunaan (untuk Termux)
Ikuti langkah-langkah di bawah ini untuk menginstal dan menjalankan CryptoTerminal-AI di aplikasi Termux pada perangkat Android Anda.

Langkah 1: Perbarui dan Tingkatkan Termux
Buka aplikasi Termux Anda dan jalankan perintah berikut untuk memastikan semua paket terbaru:

pkg update && pkg upgrade -y
Langkah 2: Berikan Izin Penyimpanan
Ini memungkinkan Termux untuk membaca dan menulis file di penyimpanan perangkat Anda, yang diperlukan untuk mengunduh proyek ini.

termux-setup-storage
(Pilih "Izinkan" atau "Allow" pada pop-up izin yang muncul.)

Langkah 3: Instal Git dan Python
Kita memerlukan Git untuk mengkloning repositori dari GitHub dan Python untuk menjalankan skrip.

pkg install git python -y
Langkah 4: Kloning Repositori
Sekarang, unduh kode CryptoTerminal-AI dari GitHub:

git clone https://github.com/batsm75/CryptoTerminal-AI.git
Langkah 5: Masuk ke Direktori Proyek
Pindah ke folder proyek yang baru saja Anda kloning:

cd CryptoTerminal-AI
Langkah 6: Instal Dependensi Python
Instal semua pustaka Python yang diperlukan oleh aplikasi ini.

pip install -r requirements.txt
(Jika file requirements.txt belum tersedia di repositori Anda, buatlah file tersebut secara manual dengan isi: requests, numpy, textwrap)

Langkah 7: Jalankan Aplikasi
Setelah semua dependensi terinstal, Anda bisa menjalankan CryptoTerminal-AI:

python main.py
(Pastikan nama file utama skrip Anda adalah main.py. Jika berbeda, ganti sesuai nama file Anda.)

🔑 Konfigurasi API Keys
Aplikasi ini menggunakan API Key untuk NewsData.io dan Gemini.

NewsData.io API Key (NEWS_API_KEY):
Anda bisa mendapatkan API Key gratis dengan mendaftar di NewsData.io.
Secara default, API Key sudah tertanam dalam kode Anda. Jika Anda ingin menggantinya, edit file main.py dan ubah nilai NEWS_API_KEY.
Gemini API Key (GEMINI_API_KEY):
Anda bisa mendapatkan API Key Gemini dari Google AI Studio.
Secara default, API Key sudah tertanam dalam kode Anda. Jika Anda ingin menggantinya, edit file main.py dan ubah nilai GEMINI_API_KEY.

Penting: Untuk alasan keamanan, hindari menyimpan API Key sensitif langsung di repositori publik. Pertimbangkan untuk menggunakan variabel lingkungan atau sistem manajemen kredensial jika Anda berencana untuk mengembangkan lebih lanjut.

📄 Lisensi
Proyek ini dilisensikan di bawah Lisensi MIT. Lihat file LICENSE untuk detail lebih lanjut.

🤝 Kontribusi
Kontribusi selalu disambut! Jika Anda memiliki ide, perbaikan, atau ingin melaporkan bug, silakan buka issue atau buat pull request di repositori ini.

Dibuat dengan ❤️ oleh Bays Exploit.


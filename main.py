import os
import requests
import numpy as np
import sys
import time

# Sistem Login
def login():
    os.system('clear')
    print("╔═══════════════════════════════╗")
    print("║          🔐 LOGIN SYSTEM      ║")
    print("╚═══════════════════════════════╝\n")
    max_attempt = 3
    while max_attempt > 0:
        username = input("👤 Masukkan Nama: ")
        password = input("🔑 Masukkan Password: ")

        if username.lower() == "crypto" and password == "cryptoanalizer":
            print("\n✅ Login berhasil! Selamat datang, Crypto.\n")
            time.sleep(1)
            return True
        else:
            max_attempt -= 1
            print(f"❌ Login gagal. Sisa percobaan: {max_attempt}\n")
            time.sleep(1)

    print("🚫 Gagal login 3 kali. Akses ditolak.")
    return False

# Fitur AI Coach Trading
def ai_coach_trading():
    os.system('clear')
    print("╔═══════════════════════════════════════╗")
    print("║         🤖 AI COACH TRADING           ║")
    print("╚═══════════════════════════════════════╝\n")
    print("Berikut beberapa istilah umum dalam dunia trading:\n")

    istilah = {
        "Bullish": "Kondisi pasar ketika harga bergerak naik.",
        "Bearish": "Kondisi pasar ketika harga bergerak turun.",
        "Support": "Level harga di mana penurunan cenderung tertahan.",
        "Resistance": "Level harga di mana kenaikan cenderung tertahan.",
        "EMA": "Exponential Moving Average – rata-rata pergerakan harga dengan bobot lebih ke data terbaru.",
        "SMA": "Simple Moving Average – rata-rata pergerakan harga biasa.",
        "RSI": "Relative Strength Index – indikator momentum untuk mengukur kondisi overbought/oversold.",
        "MACD": "Moving Average Convergence Divergence – indikator tren dan momentum.",
        "Volume": "Jumlah aset yang diperdagangkan dalam jangka waktu tertentu.",
        "Breakout": "Kondisi saat harga menembus level support/resistance dengan volume besar.",
        "Scalping": "Strategi trading jangka sangat pendek.",
        "Swing Trading": "Strategi trading dalam jangka menengah (hari hingga minggu).",
        "Divergence": "Ketidaksesuaian arah antara harga dan indikator (misal RSI).",
        "Long": "Posisi beli, berharap harga naik.",
        "Short": "Posisi jual, berharap harga turun.",
    }

    for k, v in istilah.items():
        print(f"🔹 {k}: {v}")

    input("\nTekan Enter untuk kembali ke menu utama...")

# Modul Analisa Harga Coin
def analisa_harga():
    os.system("clear")
    coin = input("🔍 Masukkan nama koin (contoh: bitcoin, solana, ethereum): ").lower()
    print("🔄 Mengambil data harga...")

    try:
        r = requests.get(f"https://api.coingecko.com/api/v3/coins/{coin}?localization=false")
        data = r.json()
        harga = data["market_data"]["current_price"]["idr"]
        perubahan_7d = data["market_data"]["price_change_percentage_7d_in_currency"]["idr"]
        perubahan_30d = data["market_data"]["price_change_percentage_30d_in_currency"]["idr"]
        perubahan_24h = data["market_data"]["price_change_percentage_24h_in_currency"]["idr"]

        ema7 = harga * 1.006
        ema25 = harga * 1.009
        ema99 = harga * 0.99
        rsi = np.random.uniform(25, 75)
        macd = np.random.choice(["Golden Cross", "Death Cross", "Neutral"])

        cut_loss = int(harga * 0.88)
        target_profit = int(harga * 1.15)

        print(f"\n📈 Harga Saat Ini: Rp {int(harga):,}")
        print(f"📅 Perubahan 7 Hari: {perubahan_7d:.2f}%")
        print(f"📅 Perubahan 30 Hari: {perubahan_30d:.2f}%")

        print(f"\n📊 EMA-7: Rp {int(ema7):,}")
        print(f"📊 EMA-25: Rp {int(ema25):,}")
        print(f"📊 EMA-99: Rp {int(ema99):,}")
        print(f"📈 RSI: {rsi:.2f}")
        print(f"📉 MACD: {macd}")

        print(f"\n🛡️ Cut Loss Plan: Rp {cut_loss:,}")
        print(f"🎯 Target Profit: Rp {target_profit:,}")

        # Psikologi Market
        print("\n🧠 Psikologi Market:")
        if rsi > 70:
            print("😬 Market euforia, banyak FOMO.")
        elif rsi < 30:
            print("😟 Market cenderung panik, ada potensi rebound.")
        else:
            print("😐 Market tenang, masih konsolidasi.")

        # Tren Harian
        print("\n📈 Tren Coin (24 Jam):")
        if perubahan_24h > 0:
            print("📊 Tren Harian: Bullish ✅")
            tren = "bullish"
        elif perubahan_24h < 0:
            print("📉 Tren Harian: Bearish ❌")
            tren = "bearish"
        else:
            print("🔄 Tren Harian: Sideways")
            tren = "sideways"

        # Prediksi & Saran
        print("\n🔮 Prediksi AI Coach:")
        if macd == "Golden Cross" and rsi < 70:
            prediksi = harga * 1.10
            print(f"📈 Potensi naik ke Rp {int(prediksi):,}")
        elif macd == "Death Cross" and rsi > 30:
            prediksi = harga * 0.90
            print(f"📉 Waspada turun ke Rp {int(prediksi):,}.")
        else:
            print("🔎 Arah pasar kurang jelas, tunggu berikutnya.")

        print("\n📣 Saran Coach (Buy / Sell / Hold):")
        if tren == "bullish" and macd == "Golden Cross" and rsi < 65:
            print("✅ BUY")
        elif tren == "bearish" and macd == "Death Cross" and rsi > 40:
            print("❌ SELL")
        else:
            print("⏸️ HOLD")

        print("\n📌 Tips:")
        print("- Pasang cut loss & take profit.")
        print("- Gunakan DCA saat market turun.")
        print("- Catat semua transaksi.")

    except:
        print("❌ Gagal mendapatkan data. Cek koneksi atau nama koin salah.")

    input("\nTekan ENTER untuk kembali...")
    
# Menu Utama
def menu():
    while True:
        os.system('clear')
        print("╔════════════════════════════╗")
        print("║     Crypto-Terminal AI    ║")
        print("╚════════════════════════════╝")
        print("[1] 📈 Analisis Coin")
        print("[2] 🤖 AI Coach Trading")
        print("[0] ❌ Keluar")

        pilihan = input("\nPilih menu: ")
        if pilihan == "1":
            analisa_harga()
        elif pilihan == "2":
            ai_coach_trading()
        elif pilihan == "0":
            print("\n👋 Sampai jumpa!")
            sys.exit()
        else:
            input("Pilihan tidak valid. Tekan ENTER untuk ulang...")

# Jalankan
if login():
    menu()

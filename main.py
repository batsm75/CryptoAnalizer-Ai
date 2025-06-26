import os
import json
import time
import requests
import numpy as np
import random
import re # Import untuk regex (cek matematika)
import textwrap # Import untuk text wrapping

# --- Konfigurasi ---
CREDENTIALS_FILE = 'credentials.json'
COINGECKO_API_BASE = 'https://api.coingecko.com/api/v3'
REFRESH_INTERVAL_SECONDS = 2 # Interval refresh data harga menjadi 2 detik

# API Key NewsData.io Anda
NEWS_API_KEY = 'pub_04af9448698b4fc89f8d13e321385574' 
NEWS_API_BASE = 'https://newsdata.io/api/1/news'

# API Key Groq (TIDAK DIGUNAKAN)
GROQ_API_KEY = 'GROQ_API_KEY_TIDAK_DIGUNAKAN' 
GROQ_API_URL = "https://api.groq.com/openai/v1/chat/completions"
GROQ_MODEL_NAME = "llama3-8b-8192" 

# API Key Gemini (untuk AI Coach Mentor di Menu 3)
GEMINI_API_KEY = 'AIzaSyDFyOGaXX75V5duTsfJFGx-S3NaFe__e5s' 
GEMINI_API_URL = "https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent"
GEMINI_MODEL_NAME = "gemini-2.0-flash"

# --- Fungsi Utilitas ---

def get_terminal_width():
    """Mendapatkan lebar terminal, dengan fallback."""
    try:
        return os.get_terminal_size().columns
    except OSError:
        return 80 # Fallback default width

def center_text(text, width):
    """Menengahkan teks dalam lebar tertentu."""
    if len(text) >= width:
        return text
    padding = (width - len(text)) // 2
    return " " * padding + text + " " * (width - len(text) - padding)

def print_wrapped(text, initial_indent="", subsequent_indent="", width=None):
    """Mencetak teks dengan wrapping otomatis sesuai lebar terminal."""
    if width is None:
        width = get_terminal_width()
    
    # Kurangi indentasi awal dan berikutnya dari lebar total
    effective_width = width - len(initial_indent)

    wrapped_lines = textwrap.fill(
        text,
        width=effective_width,
        initial_indent=initial_indent,
        subsequent_indent=subsequent_indent,
        replace_whitespace=True
    )
    print(wrapped_lines)


def clear_screen():
    """Membersihkan layar konsol."""
    os.system('clear' if os.name == 'posix' else 'cls')

def format_idr(amount):
    """Memformat angka menjadi format mata uang IDR."""
    return f"Rp {int(amount):,}".replace(",", ".")

def get_current_idr_price(coin_id):
    """Mengambil harga koin saat ini dalam IDR dari CoinGecko."""
    try:
        url = f"{COINGECKO_API_BASE}/simple/price?ids={coin_id}&vs_currencies=idr"
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()
        if coin_id in data and 'idr' in data[coin_id]:
            return data[coin_id]['idr']
        return None
    except requests.exceptions.RequestException as e:
        return None
    except json.JSONDecodeError:
        return None

def get_historical_prices(coin_id, days=90):
    """Mengambil data harga historis dari CoinGecko dan mensimulasikan OHLC."""
    try:
        url = f"{COINGECKO_API_BASE}/coins/{coin_id}/market_chart?vs_currency=idr&days={days}"
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()
        if 'prices' in data and data['prices']:
            prices_data = np.array([p[1] for p in data['prices']]) 
            
            ohlc_simulated = []
            if len(prices_data) >= 2:
                start_index = max(0, len(prices_data) - 4) # Ambil 4 harga untuk 3 candle

                for i in range(start_index + 1, len(prices_data)):
                    prev_close = prices_data[i-1]
                    current_price_for_candle = prices_data[i] 
                    
                    open_price = prev_close 
                    close_price = current_price_for_candle
                    
                    high = max(open_price, close_price) * (1 + random.uniform(0.0005, 0.002))
                    low = min(open_price, close_price) * (1 - random.uniform(0.0005, 0.002))
                    
                    ohlc_simulated.append({
                        'open': open_price,
                        'high': high,
                        'low': low,
                        'close': close_price
                    })
            
            return prices_data, ohlc_simulated
        return np.array([]), []
    except requests.exceptions.RequestException as e:
        return np.array([]), []
    except json.JSONDecodeError:
        return np.array([]), []

def get_crypto_news(query_term="crypto", num_articles=3):
    """Mengambil berita kripto dari NewsData.io API."""
    if not NEWS_API_KEY: 
        return ["⚠ Error: NEWS_API_KEY belum diatur. Harap daftar di NewsData.io untuk mendapatkan kunci API."]
        
    try:
        params = {
            'apikey': NEWS_API_KEY,
            'q': query_term,
            'language': 'en',
        }
        
        response = requests.get(NEWS_API_BASE, params=params, timeout=5)
        response.raise_for_status()
        news_data = response.json()

        articles = []
        if 'results' in news_data and news_data['results']:
            for i, article in enumerate(news_data['results']):
                if i >= num_articles:
                    break
                title = article.get('title', 'Tidak ada judul')
                articles.append(f"- {title}") 
        
        if not articles:
            articles.append("Tidak ada berita terkini yang ditemukan untuk topik ini.")
            articles.append("Coba lagi nanti atau periksa koneksi internet Anda.")
        
        return articles

    except requests.exceptions.RequestException as e:
        return [f"❌ Gagal mengambil berita: {e}. Pastikan NEWS_API_KEY benar dan ada koneksi internet."]
    except json.JSONDecodeError:
        return ["❌ Gagal mendekode respons berita dari API."]


# --- Perhitungan Indikator dengan NumPy ---

def calculate_ema_np(prices, period):
    """Menghitung Exponential Moving Average (EMA) menggunakan NumPy."""
    if len(prices) < period:
        return None
    
    k = 2 / (period + 1)
    
    ema = [np.mean(prices[:period])] 
    
    for price in prices[period:]:
        ema_val = (price * k) + (ema[-1] * (1 - k))
        ema.append(ema_val)
        
    return ema[-1]

def calculate_rsi_np(prices, period=14):
    """Menghitung Relative Strength Index (RSI) menggunakan NumPy."""
    if len(prices) < period + 1:
        return None

    deltas = np.diff(prices)
    
    gains = np.where(deltas > 0, deltas, 0)
    losses = np.where(deltas < 0, np.abs(deltas), 0)

    avg_gain = np.mean(gains[:period])
    avg_loss = np.mean(losses[:period])

    for i in range(period, len(gains)):
        avg_gain = ((avg_gain * (period - 1)) + gains[i]) / period
        avg_loss = ((avg_


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
        avg_loss = ((avg_loss * (period - 1)) + losses[i]) / period
    
    if avg_loss == 0:
        return 100.0 if avg_gain > 0 else 50.0
    
    rs = avg_gain / avg_loss
    rsi = 100 - (100 / (1 + rs))
    return rsi

def calculate_macd_np(prices, fast_period=12, slow_period=26, signal_period=9):
    """Menghitung Moving Average Convergence Divergence (MACD) menggunakan NumPy."""
    if len(prices) < max(fast_period, slow_period, signal_period) + 1:
        return "N/A"

    def _calculate_ema_series(data, period):
        if len(data) < period:
            return np.array([])
        k = 2 / (period + 1)
        ema_series = np.zeros_like(data, dtype=float)
        ema_series[period-1] = np.mean(data[:period])
        for i in range(period, len(data)):
            ema_series[i] = (data[i] * k) + (ema_series[i-1] * (1 - k))
        return ema_series[period-1:]

    ema_fast = _calculate_ema_series(prices, fast_period)
    ema_slow = _calculate_ema_series(prices, slow_period)

    min_len = min(len(ema_fast), len(ema_slow))
    if min_len == 0: return "N/A"

    macd_line = ema_fast[-min_len:] - ema_slow[-min_len:]
    
    if len(macd_line) < signal_period:
        return "N/A"

    signal_line = _calculate_ema_series(macd_line, signal_period)

    if len(macd_line) >= 2 and len(signal_line) >= 2:
        if macd_line[-1] > signal_line[-1] and macd_line[-2] <= signal_line[-2]:
            return "Golden Cross"
        elif macd_line[-1] < signal_line[-1] and macd_line[-2] >= signal_line[-2]:
            return "Death Cross"
    return "Konsolidasi"

# --- Fungsi Deteksi Pola Candlestick ---
def detect_candlestick_pattern(ohlc_data):
    """
    Mendeteksi pola candlestick dasar berdasarkan data OHLC yang disimulasikan/diperoleh.
    Ini adalah deteksi yang disederhanakan karena keterbatasan data CoinGecko gratis (tidak ada volume atau timeframe presisi).
    Akurasi sangat bergantung pada kualitas dan jumlah data OHLC yang tersedia.
    """
    patterns = []
    if not ohlc_data or len(ohlc_data) < 1:
        return [{
            "name": "DATA TIDAK CUKUP",
            "type": "Informasi Terbatas",
            "description": "Tidak ada cukup data historis yang memadai untuk mendeteksi pola candlestick. Mohon pastikan data tersedia.",
            "action": "Lanjutkan analisis indikator lain atau coba lagi nanti."
        }]
    
    last_candle = ohlc_data[-1]
    open_c = last_candle['open']
    high_c = last_candle['high']
    low_c = last_candle['low']
    close_c = last_candle['close']
    body_c = abs(close_c - open_c)
    range_total_c = high_c - low_c
    
    if range_total_c == 0:
        range_total_c = 0.0000001 
    body_ratio_to_range_c = body_c / range_total_c

    prev_candle = None
    if len(ohlc_data) >= 2:
        prev_candle = ohlc_data[-2]
    
    candle1 = None
    candle2 = None 
    if len(ohlc_data) >= 3:
        candle1 = ohlc_data[-3]
        candle2 = ohlc_data[-2] 

    # --- Pola 1-Candle ---
    # DOJI
    if body_ratio_to_range_c < 0.05:
        patterns.append({
            "name": "DOJI",
            "type": "Ketidakpastian/Netral",
            "description": "Harga pembukaan dan penutupan hampir sama, membentuk body sangat tipis. Menunjukkan keraguan ekstrem di pasar dan keseimbangan antara pembeli-penjual. Sering menjadi sinyal potensi pembalikan atau kelanjutan konsolidasi.",
            "action": "TUNGGU KONFIRMASI. Hindari posisi besar sampai arah pasar jelas."
        })
    
    # HAMMER (Bullish Reversal)
    if body_ratio_to_range_c < 0.3 and \
       (open_c - low_c) > (2 * body_c) and \
       (high_c - close_c) < (0.2 * body_c):
        patterns.append({
            "name": "HAMMER",
            "type": "Pembalikan Bullish Potensial",
            "description": "Candle dengan body kecil di bagian atas dan shadow bawah yang panjang (minimal dua kali panjang body). Ini mengindikasikan bahwa meskipun harga sempat turun signifikan, pembeli berhasil mendorongnya kembali naik. Sinyal pembalikan bullish yang kuat jika muncul setelah tren turun yang jelas.",
            "action": "Perhatikan konfirmasi bullish di candle berikutnya. Potensi BELI (LONG) jika berada di area support penting."
        })
    
    # INVERTED HAMMER (Bullish Reversal)
    elif body_ratio_to_range_c < 0.3 and \
         (high_c - close_c) > (2 * body_c) and \
         (open_c - low_c) < (0.2 * body_c):
        patterns.append({
            "name": "INVERTED HAMMER",
            "type": "Pembalikan Bullish Potensial",
            "description": "Candle dengan body kecil di bagian bawah dan shadow atas yang panjang. Menunjukkan pembeli mencoba mendorong harga naik, namun penjual sempat menekan kembali. Jika diikuti konfirmasi, bisa menjadi sinyal pembalikan bullish yang kuat setelah tren turun.",
            "action": "Perhatikan konfirmasi bullish. Potensi BELI (LONG) jika berada di area support."
        })

    # HANGING MAN (Bearish Reversal)
    if body_ratio_to_range_c < 0.3 and \
       (open_c - low_c) > (2 * body_c) and \
       (high_c - close_c) < (0.2 * body_c):
        patterns.append({
            "name": "HANGING MAN",
            "type": "Pembalikan Bearish Potensial",
            "description": "Candle dengan body kecil di bagian atas dan shadow bawah yang panjang. Muncul setelah tren naik, mengindikasikan tekanan jual mulai muncul di puncak tren. Sinyal potensi pembalikan turun dari puncak.",
            "action": "Perhatikan konfirmasi bearish di candle berikutnya. Potensi JUAL (SHORT) jika berada di area resistance penting."
        })

    # SHOOTING STAR (Bearish Reversal)
    elif body_ratio_to_range_c < 0.3 and \
         (high_c - close_c) > (2 * body_c) and \
         (open_c - low_c) < (0.2 * body_c):
        patterns.append({
            "name": "SHOOTING STAR",
            "type": "Pembalikan Bearish Potensial",
            "description": "Candle dengan body kecil di bagian bawah dan shadow atas yang panjang. Menandakan penolakan kuat di harga tinggi, penjual berhasil menekan harga kembali. Sinyal kuat pembalikan turun jika muncul setelah tren naik yang jelas.",
            "action": "Perhatikan konfirmasi bearish di candle berikutnya. Potensi JUAL (SHORT) jika berada di area resistance penting."
        })

    # --- Pola 2-Candle ---
    if prev_candle: 
        # BULLISH ENGULFING
        if prev_candle['close'] < prev_candle['open'] and \
           close_c > open_c and \
           close_c > prev_candle['open'] and \
           open_c < prev_candle['close']:
            patterns.append({
                "name": "BULLISH ENGULFING",
                "type": "Pembalikan Bullish Kuat",
                "description": "Pola dua candle: candle merah bearish (sebelumnya) diikuti oleh candle hijau bullish (saat ini) yang lebih besar dan menelan seluruh body candle merah sebelumnya. Menandakan dominasi penuh pembeli dan pembalikan tren naik yang kuat.",
                "action": "Sinyal BELI (LONG) yang kuat. Konfirmasi dengan volume tinggi jika memungkinkan."
            })
        
        # BEARISH ENGULFING
        elif prev_candle['close'] > prev_candle['open'] and \
             close_c < open_c and \
             close_c < prev_candle['open'] and \
             open_c > prev_candle['close']:
            patterns.append({
                "name": "BEARISH ENGULFING",
                "type": "Pembalikan Bearish Kuat",
                "description": "Pola dua candle: candle hijau bullish (sebelumnya) diikuti oleh candle merah bearish (saat ini) yang lebih besar dan menelan seluruh body candle hijau sebelumnya. Menandakan dominasi penuh penjual dan pembalikan tren turun yang kuat.",
                "action": "Sinyal JUAL (SHORT) yang kuat. Konfirmasi dengan volume tinggi jika memungkinkan."
            })
        
        # DARK CLOUD COVER
        elif prev_candle['close'] > prev_candle['open'] and \
             open_c > close_c and \
             open_c > prev_candle['close'] and \
             close_c < (prev_candle['open'] + prev_candle['close']) / 2: 
            patterns.append({
                "name": "DARK CLOUD COVER",
                "type": "Pembalikan Bearish Potensial",
                "description": "Pola dua candle: candle bullish kuat diikuti candle bearish yang dibuka lebih tinggi namun menutup jauh di bawah titik tengah body bullish sebelumnya. Mengindikasikan pelemahan tren naik dan potensi pembalikan turun.",
                "action": "Waspada, pertimbangkan JUAL (SHORT) jika ada konfirmasi."
            })
        
        # PIERCING PATTERN
        elif prev_candle['close'] < prev_candle['open'] and \
             close_c > open_c and \
             open_c < prev_candle['close'] and \
             close_c > (prev_candle['open'] + prev_candle['close']) / 2: 
            patterns.append({
                "name": "PIERCING PATTERN",
                "type": "Pembalikan Bullish Potensial",
                "description": "Pola dua candle: candle merah diikuti candle hijau yang dibuka lebih rendah namun menutup jauh di atas titik tengah body merah sebelumnya. Mengindikasikan pelemahan tren turun dan potensi pembalikan naik.",
                "action": "Waspada, pertimbangkan BELI (LONG) jika ada konfirmasi."
            })

    # --- Pola 3-Candle ---
    if candle1 and candle2: # Pastikan ada 3 candle untuk deteksi ini
        # MORNING STAR (Bullish Reversal)
        if candle1['close'] < candle1['open'] and \
           abs(candle2['close'] - candle2['open']) < (0.5 * abs(candle1['close'] - candle1['open'])) and \
           close_c > open_c and \
           open_c > candle2['high'] and \
           close_c > (candle1['open'] + candle1['close']) / 2 : 
            patterns.append({
                "name": "MORNING STAR",
                "type": "Pembalikan Bullish Kuat",
                "description": "Pola tiga candle: diawali candle bearish besar, diikuti candle kecil (bisa Doji/Spinning Top) yang menunjukkan keraguan, dan diakhiri candle bullish besar yang menembus ke atas. Sinyal kuat transisi dari tekanan jual ke beli.",
                "action": "Potensi BELI (LONG) yang sangat kuat setelah konfirmasi. Cari titik masuk di awal candle bullish ketiga."
            })

        # EVENING STAR (Bearish Reversal)
        elif candle1['close'] > candle1['open'] and \
             abs(candle2['close'] - candle2['open']) < (0.5 * abs(candle1['close'] - candle1['open'])) and \
             close_c < open_c and \
             open_c < candle2['low'] and \
             close_c < (candle1['open'] + candle1['close']) / 2 : 
            patterns.append({
                "name": "EVENING STAR",
                "type": "Pembalikan Bearish Kuat",
                "description": "Pola tiga candle: diawali candle bullish besar, diikuti candle kecil (bisa Doji/Spinning Top) yang menunjukkan keraguan, dan diakhiri candle bearish besar yang menembus ke bawah. Sinyal kuat transisi dari tekanan beli ke jual.",
                "action": "Potensi JUAL (SHORT) yang sangat kuat setelah konfirmasi. Cari titik masuk di awal candle bearish ketiga."
            })

    if not patterns:
        patterns.append({
            "name": "TIDAK ADA POLA SPESIFIK TERIDENTIFIKASI",
            "type": "Netral/Konsolidasi",
            "description": "Dari data historis yang tersedia, tidak ada pola candlestick reversal atau continuation yang kuat teridentifikasi. Pasar mungkin sedang dalam fase konsolidasi atau pergerakan acak. Ini bisa berarti tidak ada sinyal jelas atau data yang kurang ideal. Selalu perhatikan volume dan konfirmasi dari indikator lain.",
            "action": "Tetap HOLD atau tunggu sinyal yang lebih jelas. Lakukan riset fundamental tambahan dan pertimbangkan kondisi pasar makro."
        })
    
    return patterns

# --- Autentikasi Pengguna ---

def load_credentials():
    """Memuat kredensial dari file."""
    if os.path.exists(CREDENTIALS_FILE):
        with open(CREDENTIALS_FILE, 'r') as f:
            try:
                return json.load(f)
            except json.JSONDecodeError:
                return {}
    return {}

def save_credentials(username, password):
    """Menyimpan kredensial ke file."""
    with open(CREDENTIALS_FILE, 'w') as f:
        json.dump({'username': username, 'password': password}, f)

def register():
    """Fungsi pendaftaran pengguna."""
    width = get_terminal_width()
    clear_screen()
    print("╔" + "═" * (width - 2) + "╗")
    print("║" + center_text("📝 PENDAFTARAN AKUN", width - 2) + "║")
    print("╚" + "═" * (width - 2) + "╝\n")
    print_wrapped("Buat username dan password Anda untuk masuk.", width=width, initial_indent="")
    username = input("👤 Buat Username: ").strip()
    password = input("🔑 Buat Password: ").strip()

    if not username or not password:
        print_wrapped("❌ Username dan Password tidak boleh kosong!", width=width, initial_indent="")
        time.sleep(2)
        return False

    print_wrapped("Pendaftaran berhasil! Silakan login.", width=width, initial_indent="\n✅ ")
    time.sleep(2)
    return True

def login():
    """Fungsi login pengguna."""
    width = get_terminal_width()
    clear_screen()
    print("╔" + "═" * (width - 2) + "╗")
    print("║" + center_text("🔐 SISTEM LOGIN", width - 2) + "║")
    print("╚" + "═" * (width - 2) + "╝\n")
    credentials = load_cre

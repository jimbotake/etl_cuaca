import requests
import psycopg2
from datetime import datetime
import os
from dotenv import load_dotenv

# Load konfigurasi dari file .env
load_dotenv()

print("API_KEY:", os.getenv("API_KEY"))
print("CITY:", os.getenv("CITY"))


API_KEY = os.getenv('API_KEY')
CITY = os.getenv('CITY')

URL = f'http://api.weatherapi.com/v1/current.json?key={API_KEY}&q={CITY}&aqi=no'

# Konfigurasi database PostgreSQL
DB_CONFIG = {
    'dbname': os.getenv('DB_NAME'),
    'user': os.getenv('DB_USER'),
    'password': os.getenv('DB_PASS'),
    'host': os.getenv('DB_HOST'),
    'port': os.getenv('DB_PORT')
}

# Ambil data dari API
response = requests.get(URL)
data = response.json()

print("DB Config:", DB_CONFIG)

# DEBUG: tampilkan isi data dari API
if 'error' in data:
    print("❌ API Error:", data['error']['message'])
    exit()

if 'current' not in data:
    print("❌ Response tidak mengandung data cuaca:")
    print(data)
    exit()

# Ambil data cuaca
weather_data = {
    'city': CITY,
    'temperature': data['current']['temp_c'],
    'humidity': data['current']['humidity'],
    'pressure': data['current']['pressure_mb'],
    'condition': data['current']['condition']['text'],
    'wind_kph': data['current']['wind_kph'],
    'timestamp': datetime.strptime(data['location']['localtime'], "%Y-%m-%d %H:%M")
}

# Simpan ke PostgreSQL
try:
    conn = psycopg2.connect(**DB_CONFIG)
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS weather_data (
            id SERIAL PRIMARY KEY,
            city VARCHAR(100),
            temperature FLOAT,
            humidity INT,
            pressure INT,
            condition TEXT,
            wind_kph FLOAT,
            timestamp TIMESTAMP
        )
    """)

    cursor.execute("""
        INSERT INTO weather_data (city, temperature, humidity, pressure, condition, wind_kph, timestamp)
        VALUES (%s, %s, %s, %s, %s, %s, %s)
    """, tuple(weather_data.values()))

    conn.commit()
    cursor.close()
    conn.close()

    print("✅ Data cuaca berhasil disimpan ke PostgreSQL.")
except Exception as e:
    print("❌ Gagal menyimpan ke database:", e)

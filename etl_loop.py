import requests
import psycopg2
from datetime import datetime
import os
from dotenv import load_dotenv
import time

# Load konfigurasi dari .env
load_dotenv()

API_KEY = os.getenv('API_KEY')
CITY = os.getenv('CITY')

URL = f'http://api.weatherapi.com/v1/current.json?key={API_KEY}&q={CITY}&aqi=no'

DB_CONFIG = {
    'dbname': os.getenv('DB_NAME'),
    'user': os.getenv('DB_USER'),
    'password': os.getenv('DB_PASS'),
    'host': os.getenv('DB_HOST'),
    'port': os.getenv('DB_PORT')
}

def run_etl():
    print(f"Menjalankan ETL ambil data cuaca untuk kota {CITY} ...")
    try:
        response = requests.get(URL)
        data = response.json()

        if 'error' in data:
            print("❌ API Error:", data['error']['message'])
            return

        if 'current' not in data:
            print("❌ Response tidak mengandung data cuaca:", data)
            return

        weather_data = {
            'city': CITY,
            'temperature': data['current']['temp_c'],
            'humidity': data['current']['humidity'],
            'pressure': data['current']['pressure_mb'],
            'condition': data['current']['condition']['text'],
            'wind_kph': data['current']['wind_kph'],
            'timestamp': datetime.strptime(data['location']['localtime'], "%Y-%m-%d %H:%M")
        }

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
        print("❌ Gagal menjalankan ETL:", e)


if __name__ == "__main__":
    interval = 60  # jeda antar ETL dalam detik, bisa ubah sesuai kebutuhan
    runs = 10      # mau jalankan berapa kali

    for i in range(runs):
        print(f"\nRun ke-{i+1} dimulai")
        run_etl()
        if i < runs - 1:
            print(f"Tunggu {interval} detik sebelum run berikutnya...")
            time.sleep(interval)
    print("\nSelesai semua run ETL.")

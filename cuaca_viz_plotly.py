import psycopg2
import pandas as pd
import plotly.express as px
from dotenv import load_dotenv
import os

# Load konfigurasi .env
load_dotenv()

DB_CONFIG = {
    'dbname': os.getenv('DB_NAME'),
    'user': os.getenv('DB_USER'),
    'password': os.getenv('DB_PASS'),
    'host': os.getenv('DB_HOST'),
    'port': os.getenv('DB_PORT')
}

try:
    # Koneksi ke database
    conn = psycopg2.connect(**DB_CONFIG)

    # Ambil data cuaca terbaru, misal 100 data
    query = """
    SELECT timestamp, temperature, humidity, pressure, wind_kph FROM weather_data
    ORDER BY timestamp DESC
    LIMIT 100;
    """

    df = pd.read_sql_query(query, conn)
    conn.close()

    # Balik urutan agar dari waktu terlama ke terbaru
    df = df.iloc[::-1]

    # Buat grafik suhu interaktif dengan Plotly
    fig = px.line(df, x='timestamp', y='humidity', title='Kelembaban Cuaca Terbaru',
              labels={'timestamp': 'Waktu', 'humidity': 'Kelembaban (%)'},
              markers=True)


    # Tampilkan grafik
    fig.show()

except Exception as e:
    print("❌ Gagal ambil data atau visualisasi:", e)

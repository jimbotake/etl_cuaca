import psycopg2
import pandas as pd
import matplotlib.pyplot as plt
from dotenv import load_dotenv
import os

# Load konfigurasi dari file .env
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
    
    # Query data cuaca, misal ambil 50 data terbaru
    query = """
    SELECT timestamp, temperature FROM weather_data
    ORDER BY timestamp DESC
    LIMIT 50;
    """
    
    df = pd.read_sql_query(query, conn)
    conn.close()

    # Balik urutan supaya dari yang paling lama ke terbaru
    df = df.iloc[::-1]
    
    # Plot grafik suhu
    plt.figure(figsize=(10,5))
    plt.plot(df['timestamp'], df['temperature'], marker='o')
    plt.title('Suhu Cuaca Terbaru')
    plt.xlabel('Waktu')
    plt.ylabel('Suhu (°C)')
    plt.grid(True)
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.show()

except Exception as e:
    print("❌ Gagal ambil data atau visualisasi:", e)

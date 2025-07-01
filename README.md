
# 🌦️ Proyek ETL Data Cuaca (WeatherAPI → PostgreSQL)

Proyek ini mengambil data cuaca real-time dari WeatherAPI dan menyimpannya ke PostgreSQL menggunakan Python. Cocok untuk latihan data engineering sederhana. Loop Otomatis tiap menit. Visualisasi dengan Plotly

## 🚀 Teknologi yang Digunakan
- Python 3.10
- PostgreSQL
- WeatherAPI (https://www.weatherapi.com/)
- Library: `requests`, `psycopg2-binary`, `python-dotenv`

## 🧱 Struktur Proyek

```
etl_cuaca/
├── etl_weatherapi.py       # Script utama ETL
├── config.env              # Simpan API key dan DB config
├── requirements.txt        # Daftar dependensi Python
├── README.md               # Deskripsi proyek
└── .gitignore              # File ignore Git
```

## ⚙️ Langkah Instalasi

### 1. Clone repository atau download folder

```bash
git clone <repo-url>
cd etl_cuaca
```

### 2. Buat virtual environment dengan conda (opsional tapi disarankan)

```bash
conda create -n etl_cuaca python=3.10
conda activate etl_cuaca
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Siapkan file `.env`

Buat file `config.env` dengan isi:

```
API_KEY=your_api_key
CITY=Jakarta

DB_NAME=weather_db
DB_USER=postgres
DB_PASS=your_password
DB_HOST=localhost
DB_PORT=5432
```

### 5. Jalankan ETL

```bash
python etl_weatherapi.py
```

## 📌 Catatan

- Pastikan PostgreSQL sudah berjalan dan database `weather_db` sudah dibuat.
- API Key bisa didapat dari https://www.weatherapi.com/ (paket gratis tersedia).

## 📊 Output

Tabel di PostgreSQL bernama `weather_data` dengan kolom:
- city, temperature, humidity, pressure, condition, wind_kph, timestamp

---

## 🛠️ Lisensi

MIT License

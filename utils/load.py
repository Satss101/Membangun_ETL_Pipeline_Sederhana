import pandas as pd
from sqlalchemy import create_engine

def save_to_csv(dataframe):
    """Menyimpan DataFrame ke file CSV lokal."""
    dataframe.to_csv("products.csv", index=False)
    print("Data berhasil disimpan ke file CSV")

def save_to_postgresql(dataframe):
    """Menyimpan DataFrame ke dalam tabel PostgreSQL."""
    try:
        # Konfigurasi koneksi ke database PostgreSQL
        db_username = 'satss'
        db_password = '121'
        db_host = 'localhost'
        db_port = '5432'
        db_name = 'product_db'

        # Buat koneksi ke PostgreSQL menggunakan SQLAlchemy
        engine = create_engine(f'postgresql+psycopg2://{db_username}:{db_password}@{db_host}:{db_port}/{db_name}')

        # Simpan DataFrame ke dalam tabel PostgreSQL (replace = timpa jika tabel sudah ada)
        dataframe.to_sql('products', engine, if_exists='replace', index=False)
        print(f"Data berhasil disimpan ke PostgreSQL")

    except Exception as error:
        print(f"Gagal menyimpan data ke PostgreSQL: {error}")
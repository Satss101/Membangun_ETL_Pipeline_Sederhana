import pandas as pd
import numpy as np
from datetime import datetime

toRP = 16000

def clean_and_transform_data(raw_products):
    """Membersihkan dan mengubah data ke dalam bentuk DataFrame yang terstruktur."""
    df = pd.DataFrame(raw_products)

    # Filter baris dengan judul tidak valid seperti "unknown"
    if 'title' in df.columns:
        df = df[~df['title'].str.lower().str.contains('unknown', na=False)]
        # Hapus angka di akhir judul produk
        df['title'] = df['title'].str.replace(r'\s+\d+$', '', regex=True)  

    # Bersihkan dan konversi harga ke float dalam IDR
    df['price'] = df['price'].replace(r'[^\d.]', '', regex=True).replace('', np.nan)
    df.dropna(subset=['price'], inplace=True)
    df['price'] = df['price'].astype(float) * toRP

    # Bersihkan dan ubah kolom rating menjadi float dengan 1 angka desimal (tanpa pembulatan ke atas)
    df['rating'] = df['rating'].replace(r'[^0-9.]', '', regex=True).replace('', np.nan)
    df.dropna(subset=['rating'], inplace=True)
    df['rating'] = df['rating'].astype(float)
    df['rating'] = df['rating'].apply(lambda x: float(str(x)[:str(x).find('.')+2]) if '.' in str(x) else float(x))

    # Bersihkan dan konversi kolom colors menjadi int64
    df['colors'] = df['colors'].replace(r'[^0-9]', '', regex=True).replace('', np.nan)
    df.dropna(subset=['colors'], inplace=True)
    df['colors'] = df['colors'].astype('int64')

    # Hilangkan label teks dari kolom size dan gender
    df['size'] = df['size'].replace(r'Size:\s*', '', regex=True)
    df['gender'] = df['gender'].replace(r'Gender:\s*', '', regex=True)

    # Hapus baris duplikat dan nilai kosong
    df.drop_duplicates(inplace=True)
    df.dropna(inplace=True)

    # Tambahkan kolom timestamp
    df['timestamp'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    df['timestamp'] = pd.to_datetime(df['timestamp'])
    df['timestamp'] = df['timestamp'].dt.tz_localize('Asia/Jakarta')

    return df

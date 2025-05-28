from utils.extract import extract_data_from_page
from utils.transform import clean_and_transform_data
from utils.load import save_to_csv, save_to_postgresql

def main():
    """Main function to run the ETL process: Extract, Transform, Load."""
    
    base_url = 'https://fashion-studio.dicoding.dev/'
    collected_products = []

    # Mulai scraping dari halaman utama
    print(f"Memulai scraping dari halaman utama: {base_url}")
    try:
        products = extract_data_from_page(base_url)
        collected_products.extend(products)
    except Exception as e:
        print(f"Gagal mengambil data dari halaman utama: {e}")

    # Lanjutkan scraping dari halaman 2 sampai 50
    for page in range(2, 51):
        page_url = f"{base_url}page{page}"
        print(f"Scraping halaman ke-{page}: {page_url}")
        try:
            products = extract_data_from_page(page_url)
            collected_products.extend(products)
        except Exception as e:
            print(f"Gagal mengambil data dari halaman {page}: {e}")

    # Jika tidak ada data yang berhasil diambil, hentikan program
    if not collected_products:
        print("Tidak ada data produk yang berhasil diambil. Program dihentikan.")
        return

    # Bersihkan dan transformasi data hasil scraping
    cleaned_data = clean_and_transform_data(collected_products)

    # Simpan data yang telah dibersihkan ke file CSV
    save_to_csv(cleaned_data)

    # Simpan data yang telah dibersihkan ke database PostgreSQL
    save_to_postgresql(cleaned_data)

    # Proses selesai
    print("Proses scraping dan penyimpanan data selesai.")

# Jalankan fungsi utama
if __name__ == "__main__":
    main()

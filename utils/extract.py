import requests
from bs4 import BeautifulSoup

HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
        "(KHTML, like Gecko) Chrome/96.0.4664.110 Safari/537.36"
    )
}

def extract_product_data(card):
    # Ambil informasi produk dari elemen HTML
    title = card.find('h3', class_='product-title')
    price = card.find('div', class_='price-container')
    rating = card.find('p', string=lambda t: t and 'Rating' in t)
    colors = card.find('p', string=lambda t: t and 'Colors' in t)
    size = card.find('p', string=lambda t: t and 'Size' in t)
    gender = card.find('p', string=lambda t: t and 'Gender' in t)

    # Susun data ke dalam dictionary
    product = {
        'title': title.text.strip() if title else 'Unknown Title',
        'price': price.text.strip() if price else 'Price Not Available',
        'rating': rating.text.strip() if rating else 'No Rating',
        'colors': colors.text.strip() if colors else 'No Color Info',
        'size': size.text.strip() if size else 'No Size Info',
        'gender': gender.text.strip() if gender else 'No Gender Info',
    }

def fetch_page_content(url):
    """"Mengambil konten HTML dari URL yang diberikan dengan penanganan kesalahan."""
    try:
        # Kirim permintaan HTTP ke halaman
        response = requests.get(url, headers=HEADERS, timeout=10)
        response.raise_for_status()
        return response.content
    except requests.exceptions.RequestException as error:
        print(f"Error saat mengambil {url}: {error}")
        return None

def extract_data_from_page(url):
    """Mengambil data produk dari halaman koleksi berdasarkan URL."""
    response = fetch_page_content(url)
    if not response:
        return []
    
    try:
        # Parsing isi halaman dengan BeautifulSoup
        soup = BeautifulSoup(response.text, 'html.parser')
        data = []

        # Temukan semua elemen kartu produk
        cards = soup.find_all('div', class_='collection-card')
        if not cards:
            print(f"Tidak ada produk ditemukan di halaman {url}")

        for card in cards:
            product = extract_product_data(card)
            data.append(product)

        print(f"{len(data)} produk berhasil diambil dari {url}")
        return data

    except Exception as parse_error:
        raise Exception(f"Terjadi kesalahan saat parsing HTML: {parse_error}")

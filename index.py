import requests
from bs4 import BeautifulSoup

# Base URL
base_url = 'https://istanbulmobilyafuari.com/katilimci-listesi?page={}'

# Iterate over pages from 1 to 69
for page_number in range(1, 70):
    # Construct the URL for the current page
    url = base_url.format(page_number)

    # Sayfayı indir
    response = requests.get(url)

    # Hata kontrolü
    if response.status_code == 200:
        # HTML içeriğini parse et
        soup = BeautifulSoup(response.content, 'html.parser', from_encoding='utf-8')

        # data-title="Firma Adı" ve class="table-block-content" olan öğeyi çek
        firma_adlari = soup.select('.filter-list__item tbody tr')

        # Bulunan elementlerin içeriğini yazdır ve index.txt dosyasına ekleyin
        with open('index.txt', 'a', encoding='utf-8') as file:
            for firma in firma_adlari:
                firma_adi = firma.text.strip()
                print(firma_adi)
                file.write(firma_adi + '\n')

        print(f'Page {page_number}: Veriler index.txt dosyasına eklenerek kaydedildi.')
    else:
        print(f'Page {page_number}: Hata: {response.status_code}')

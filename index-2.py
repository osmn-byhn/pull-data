import requests
from bs4 import BeautifulSoup

url = 'https://istanbulmobilyafuari.com/katilimci-listesi?participantFullList=true'

# Sayfayı indir
response = requests.get(url)

# Hata kontrolü
if response.status_code == 200:
    # HTML içeriğini parse et
    soup = BeautifulSoup(response.content, 'html.parser', from_encoding='utf-8')

    # data-title="Firma Adı" ve class="table-block-content" olan öğeyi çek
    firma_adlari = soup.select('.filter-table-zebra tbody tr [data-title="Firma Adı"]')

    # Bulunan elementlerin içeriğini yazdır ve index.txt dosyasına ekleyin
    with open('index-2.txt', 'a', encoding='utf-8') as file:
        for firma in firma_adlari:
            firma_adi = firma.text.strip()
            print(firma_adi)
            file.write(firma_adi + '\n')

    print('Veriler index-2.txt dosyasına eklenerek kaydedildi.')
else:
    print(f'Hata: {response.status_code}')

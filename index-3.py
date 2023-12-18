import requests
from bs4 import BeautifulSoup
import pandas as pd

url = 'https://istanbulmobilyafuari.com/katilimci-listesi'

# Sayfayı indir
response = requests.get(url)

# Hata kontrolü
if response.status_code == 200:
    # HTML içeriğini parse et
    soup = BeautifulSoup(response.content, 'html.parser', from_encoding='utf-8')

    # .responsive-table içindeki <thead> içindeki <tr> içindeki <th> elementlerini bul
    thead = soup.select('.responsive-table thead tr th')
    headers = [th.text.strip() for th in thead]

    # .responsive-table içindeki <tbody> içindeki <tr> içindeki <td> elementlerini bul
    tbody = soup.select('.responsive-table tbody tr')

    # Verileri bir liste olarak topla
    rows = []
    for tr in tbody:
        row_data = [td.text.strip() for td in tr.find_all('td')]
        if len(row_data) == len(headers):
            rows.append(row_data)

    # DataFrame'i oluşturun
    df = pd.DataFrame(rows, columns=headers)

    # DataFrame'i Excel dosyasına yazın
    df.to_excel('veriler.xlsx', index=False)

    print('Veriler veriler.xlsx dosyasına kaydedildi.')
else:
    print(f'Hata: {response.status_code}')

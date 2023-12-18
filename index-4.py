import re
import pandas as pd

# Read the lines from the index.txt file
with open('index.txt', 'r', encoding='utf-8') as file:
    lines = file.readlines()

# Initialize empty lists to store data
firma_adi_list = []
adres_list = []
telefon_list = []
webadresi_list = []
salon_list = []
urun_gruplari_list = []

# Flags for handling DETAYLAR and SALON sections
skip_next_lines = False
salon_section = False
urun_gruplari_section = False

# Keywords to identify lines that should be combined under 'Firma Adı'
keywords_to_combine = ["TAAH", "SAN", "TİC", "LTD", "ŞTİ"]

# Initialize current variables
current_firma_adi = ""
current_adres = ""
current_telefon = ""
current_webadresi = ""
current_salon = ""
current_urun_gruplari = ""

# Function to check if the line contains any of the specified keywords
def contains_keywords(line):
    return any(keyword in line for keyword in keywords_to_combine)

# Iterate through lines and extract information
for line in lines:
    line = line.strip()

    if skip_next_lines:
        skip_next_lines = False
        continue

    if line.startswith('İletişim:'):
        telefon_match = re.search(r'\+[\d\s\(\)-]+', line)
        current_telefon = telefon_match.group() if telefon_match else ""
    elif line.startswith('Web:'):
        current_webadresi = line[len('Web:'):].strip()
    elif line == 'DETAYLAR':
        # Set the flag to skip the DETAYLAR section
        skip_next_lines = True
    elif line.startswith('Salon:'):
        salon_section = True
        current_salon = line[len('Salon:'):].strip()
    elif salon_section and line.startswith('Stant:'):
        # If the line starts with 'Stant:', include the salon information
        current_salon += " " + line[len('Stant:'):].strip()
        salon_section = False
    elif contains_keywords(line) or "Ürün Grupları" in line:
        # Combine lines containing specified keywords under 'Firma Adı'
        current_firma_adi += " " + line
        urun_gruplari_section = True
    elif urun_gruplari_section:
        if line:
            current_urun_gruplari += " " + line
        else:
            urun_gruplari_section = False
            urun_gruplari_list.append(current_urun_gruplari.strip())
            current_urun_gruplari = ""
    elif "Merkez" in line:
        # Skip lines containing "Merkez"
        continue
    elif line:
        if not current_firma_adi:
            current_firma_adi = line
        else:
            current_adres += line + ' '

    elif not line and current_firma_adi:
        firma_adi_list.append(current_firma_adi.strip())
        adres_list.append(current_adres.strip())
        telefon_list.append(current_telefon)
        webadresi_list.append(current_webadresi)
        salon_list.append(current_salon)
        
        # Check if urun_gruplari_list has the same length as other lists
        if len(urun_gruplari_list) != len(firma_adi_list):
            urun_gruplari_list.append("")  # Add an empty string to match lengths
       
        # Reset current variables for the next entry
        current_firma_adi = ""
        current_adres = ""
        current_telefon = ""
        current_webadresi = ""
        current_salon = ""

# Create a DataFrame
df = pd.DataFrame({
    'Firma Adı': firma_adi_list,
    'Adres': adres_list,
    'Telefon': telefon_list,
    'Web Adresi': webadresi_list,
    'Salon': salon_list,
    'Ürün Grupları': urun_gruplari_list
})

# Save the DataFrame to an Excel file
df.to_excel('index_with_urun_gruplari.xlsx', index=False)

print('Veriler index_with_urun_gruplari.xlsx dosyasına kaydedildi.')

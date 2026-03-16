import requests
from bs4 import BeautifulSoup

url = "https://www.bceao.int/fr/publications/bilans-et-comptes-de-resultat-des-banques-etablissements-financiers-et-compagnies"

response = requests.get(url)

print(response.status_code)

soup = BeautifulSoup(response.text, "html.parser")

print(soup.title)

links = soup.find_all("a")

pdf_links = set()

base_url = "https://www.bceao.int"

for link in links:

    href = link.get("href")

    if href and ".pdf" in href:

        if href.startswith("/"):
            href = base_url + href

        pdf_links.add(href)


print("PDF uniques :", len(pdf_links))

for pdf in pdf_links:
    print(pdf)

    
import os

folder = "data/raw_pdf"

os.makedirs(folder, exist_ok=True)

for link in pdf_links:

    filename = link.split("/")[-1]

    try:
        r = requests.get(link)

        with open(f"{folder}/{filename}", "wb") as f:
            f.write(r.content)

        print("Téléchargé :", filename)

    except:
        print("Erreur :", link)
import requests
import os

pdf_links = [
    "lien1.pdf",
    "lien2.pdf"
]

folder = "data/raw_pdf"

os.makedirs(folder, exist_ok=True)

for link in pdf_links:

    filename = link.split("/")[-1]

    r = requests.get(link)

    with open(f"{folder}/{filename}", "wb") as f:
        f.write(r.content)

print("Téléchargement terminé")
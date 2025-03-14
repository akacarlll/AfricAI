import os
import requests
from bs4 import BeautifulSoup
import re
from urllib.parse import unquote
from scraping_bots.cmr_bots.extras.scraping_function import (
    generate_file_name,
    get_page_title,
    categorize_file,
)


def download_pdfs(pdf_urls):
    """Downloads all PDF files from the given URLs and saves them to a specified directory.

    Args: pdf_urls (list): List of tuples of URLs pointing to PDF files and the page of the pdf file.

    Saves each PDF to the directory defined within the function.
    """
    base_folder = r"C:\Users\carlf\Documents\GitHub\LawIntelAfrica\data\01_raw\cmr\pdfs"
    if not os.path.exists(base_folder):
        os.makedirs(base_folder)

    for pdf_url, page_url in pdf_urls:
        try:
            response = requests.get(page_url)
            response.raise_for_status()
            soup = BeautifulSoup(response.text, "html.parser")
            title_element = soup.find("h2", class_="main-title")
            if title_element:
                title = title_element.get_text(strip=True)
                title_on_page = get_page_title(title)
                pdf_name = generate_file_name(title_on_page)
            else:
                pdf_name = pdf_url.split("/")[-1]

            category = categorize_file(pdf_name)

            destination_folder = os.path.join(base_folder, category)
            os.makedirs(
                destination_folder, exist_ok=True
            )  # Créer le dossier si inexistant

            # Définir le chemin complet du fichier PDF
            destination_path = os.path.join(destination_folder, f"{pdf_name}.pdf")

            response = requests.get(pdf_url, stream=True)
            response.raise_for_status()

            with open(destination_path, "wb") as pdf_file:
                for chunk in response.iter_content(chunk_size=8192):
                    pdf_file.write(chunk)

        except Exception as e:
            print(f"Erreur lors du téléchargement de {pdf_url}: {e}")

        print(f"✅ Pdf downloaded to file: {destination_path}")

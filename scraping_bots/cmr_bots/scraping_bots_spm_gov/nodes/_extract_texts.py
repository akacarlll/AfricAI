import os
import requests
from bs4 import BeautifulSoup
from urllib.parse import unquote
from scraping_bots.cmr_bots.extras.scraping_function import save_file, generate_file_name, get_page_title, categorize_file

def extract_text(urls):
    """
    Downloads the text from all <p> tags of the given pages and creates a file for each page.
    Uses the page title (<h2 class="main-title">) as the file name.

    Arguments:
    - urls (list): List of URLs of the pages containing text.
    """
    base_folder = r"C:\Users\carlf\Documents\GitHub\LawIntelAfrica\data\01_raw\cmr\texts"
    os.makedirs(base_folder, exist_ok=True)

    for url in urls:
        try:
            response = requests.get(url)
            response.raise_for_status()
            soup = BeautifulSoup(response.text, 'html.parser')

            # Extraction du titre
            title_element = soup.find('h2', class_='main-title')
            if title_element:
                title = title_element.get_text(strip=True)
                title_on_page = get_page_title(title)
                file_name = generate_file_name(title_on_page)
            else:
                file_name = "page_without_title"
                title_on_page = "Unknown"
            category = categorize_file(file_name)



            sub_folder = os.path.join(base_folder, category)
            os.makedirs(sub_folder, exist_ok=True)  # Création du dossier si inexistant
            
            # Définition du chemin du fichier
            file_path = os.path.join(sub_folder, f"{file_name}.csv")

            # Extraction du texte des paragraphes
            paragraphs = soup.find_all('p')
            text = "\n".join(p.get_text(strip=True) for p in paragraphs)
            
            save_file(file_path, url, text, title_on_page)

            print(f"✅ Fichier enregistré : {file_path}")

        except Exception as e:
            print(f"❌ Erreur lors du traitement de {url}: {e}")

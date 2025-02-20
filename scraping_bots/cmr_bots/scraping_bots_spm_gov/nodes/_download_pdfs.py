import os
import requests
from bs4 import BeautifulSoup
import re
from urllib.parse import unquote


def download_pdfs(pdf_urls):
    """ Downloads all PDF files from the given URLs and saves them to a specified directory.

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
            soup = BeautifulSoup(response.text, 'html.parser')
            title_element = soup.find('h2', class_='main-title')
            if title_element:
                title = title_element.get_text(strip=True)
                title_on_page = get_page_title(title)
                pdf_name = generate_file_name(title_on_page)
            else:
                pdf_name = pdf_url.split("/")[-1]
            
            category = "autres"  # Valeur par défaut
            if "decret" in pdf_name.lower():
                category = "decret"
            elif "arrete" in pdf_name.lower():
                category = "arrete"
            elif "circulaire" in pdf_name.lower():
                category = "circulaire"
            elif "loi" in pdf_name.lower():
                category = "loi"
            destination_folder = os.path.join(base_folder, category)
            os.makedirs(destination_folder, exist_ok=True)  # Créer le dossier si inexistant

            # Définir le chemin complet du fichier PDF
            destination_path = os.path.join(destination_folder, f"{pdf_name}.pdf")

            response = requests.get(pdf_url, stream=True)
            response.raise_for_status()

            with open(destination_path, 'wb') as pdf_file:
                for chunk in response.iter_content(chunk_size=8192):
                    pdf_file.write(chunk)

        except Exception as e:
            print(f"Erreur lors du téléchargement de {pdf_url}: {e}")
            
def get_page_title(title):
    """
    Generates a file name from a page title, with intelligent truncation.

    If the full title exceeds 100 characters, it truncates at the last underscore
    before the length exceeds 100 characters.

    Arguments:
    - title (str): The page title.

    Returns:
    - str: The adapted file name.
    """
    cleaned_title = unquote(title).replace("/", "_").replace("\\", "_").replace("?", "_").replace("&", "_").replace(":", "_").replace(" ", "_").replace("é", "e").replace("ê", "e").replace("É", "E").replace("È", "E").replace("Ê", "E").replace("£", "E")

    if len(cleaned_title) > 200:
        last_underscore = cleaned_title[:200].rfind("_")
        if last_underscore != -1:
            cleaned_title = cleaned_title[:last_underscore]
        else:
            cleaned_title = cleaned_title[:200]
    
    return cleaned_title

def generate_file_name(text):
    # Trouver toutes les occurrences de 4 chiffres consécutifs
    numbers = re.findall(r'\d{4}', text)

    # Filtrer pour ne garder que celles qui ressemblent à des années (1900-2100)
    years = [num for num in numbers if 1900 <= int(num) <= 2100]

    if len(years) >= 2:  # Vérifier s'il y a au moins deux années valides
        second_year = years[1]  # Prendre la deuxième année trouvée
        split_index = text.rfind(second_year) + len(second_year)  # Trouver la DERNIÈRE occurrence de cette année
        return text[:split_index]  # Garder uniquement la partie avant et incluant la deuxième année
    
    return text  # Retourne la chaîne entière si pas assez d'années valides

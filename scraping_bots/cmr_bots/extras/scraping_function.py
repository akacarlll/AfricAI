import os
import requests
from bs4 import BeautifulSoup
import csv
from urllib.parse import unquote
import re
import csv


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
    
    cleaned_title = unquote(title).replace("/", "_").replace("\\", "_").replace("?", "_") \
        .replace("&", "_").replace(":", "_").replace(" ", "_").replace("é", "e") \
        .replace("ê", "e").replace("É", "E").replace("È", "E").replace("Ê", "E") \
        .replace("£", "E").replace('"', '_').replace("'", "_")

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


def save_file(file_path, url, text, title_on_page) -> None:
    
    with open(file_path, mode='w', newline='', encoding='utf-8') as csv_file:
        writer = csv.writer(csv_file)
        writer.writerow(["URL", "text", "page_title"])
        writer.writerow([url, text, title_on_page])

    print(f"Text extracted and added to file: {file_path}")
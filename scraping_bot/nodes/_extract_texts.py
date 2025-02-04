import os
import csv
import requests
from bs4 import BeautifulSoup
from urllib.parse import urlparse, unquote

def extract_text(urls):
    """
    Télécharge le texte de toutes les balises <p> des pages données et crée un fichier pour chaque page.
    Utilise le titre de la page (<h2 class="main-title">) comme nom de fichier.
    
    Arguments :
    - urls (list) : Liste des URLs des pages contenant du texte.
    """
    # Dossier pour stocker les fichiers CSV individuels
    dossier_destination = r"C:\Users\carlf\Documents\GitHub\LawIntelAfrica\data\01_raw\texts"
    os.makedirs(dossier_destination, exist_ok=True)

    for url in urls:
        try:
            # Faire la requête et parser la page
            response = requests.get(url)
            response.raise_for_status()
            soup = BeautifulSoup(response.text, 'html.parser')

            # Extraire le titre
            titre_element = soup.find('h2', class_='main-title')
            if titre_element:
                titre = titre_element.get_text(strip=True)
                # Nettoyer le titre pour un nom de fichier valide
                titre_fichier = unquote(titre).replace("/", "-").replace("\\", "-").replace("?", "-").replace("&", "-").replace(":", "-").replace(" ", "_")
            else:
                # Fallback si aucun titre trouvé
                titre_fichier = "page_sans_titre"
            
            # Générer un chemin complet pour le fichier
            fichier_nom = f"{titre_fichier}.csv"
            chemin_fichier = os.path.join(dossier_destination, fichier_nom)

            # Extraire tout le texte des balises <p>
            paragraphes = soup.find_all('p')
            texte = "\n".join(p.get_text(strip=True) for p in paragraphes)
            
            # Écrire l'URL et le texte dans le fichier CSV
            with open(chemin_fichier, mode='w', newline='', encoding='utf-8') as fichier_csv:
                writer = csv.writer(fichier_csv)
                writer.writerow(["URL", "Texte"])
                writer.writerow([url, texte])
            
            print(f"Texte extrait et ajouté au fichier : {chemin_fichier}")
        
        except Exception as e:
            print(f"Erreur lors du traitement de {url}: {e}")

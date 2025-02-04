import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin

def extract_pages_urls(url):
    """
    Extrait toutes les URLs des liens sur une page donnée.
    Gère les cas où certains éléments peuvent être manquants.
    
    Args:
        url (str): URL de la page à scraper
        
    Returns:
        list: Liste des URLs complètes trouvées sur la page
    """
    # Liste pour stocker les URLs
    urls = []
    
    try:
        # Faire la requête
        response = requests.get(url)
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # Trouver tous les divs de type 'views-row'
        rows = soup.find_all('div', class_='views-row')
        
        # Pour chaque row, extraire l'URL de façon sécurisée
        for row in rows:
            # Chercher le h3 d'abord
            h3_tag = row.find('h3')
            if h3_tag:  # Si h3 existe
                link = h3_tag.find('a')
                if link and 'href' in link.attrs:
                    # Construire l'URL complète
                    full_url = urljoin("https://www.spm.gov.cm", link['href'])
                    urls.append(full_url)
                    
        return urls
        
    except Exception as e:
        print(f"Erreur lors de l'extraction des URLs: {str(e)}")
        return []
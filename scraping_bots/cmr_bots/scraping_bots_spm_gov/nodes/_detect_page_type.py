import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
import time


def detect_page_type(urls):
    """
    Determines if a page contains a downloadable PDF or text.

    Args:
        urls (list): List of URLs to analyze.

    Returns:
        tuple: (text_page_type, pdf_page_type)
            - text_page_type: List of URLs containing text to copy.
            - pdf_page_type: List of tuples (pdf_url, page_url).
    """
    pdf_page_type = []
    text_page_type = []

    for url in urls:
        try:
            # Faire la requête
            response = requests.get(url)
            soup = BeautifulSoup(response.text, "html.parser")

            # Chercher un lien PDF dans la page
            pdf_link = soup.find("a", type=lambda x: x and "pdf" in x.lower())

            if pdf_link and "href" in pdf_link.attrs:
                # Construire l'URL complète du PDF
                pdf_url = urljoin(url, pdf_link["href"])
                pdf_page_type.append((pdf_url, url))
            else:
                # Si aucun PDF n'est trouvé, considérer la page comme du texte
                text_page_type.append(url)

            time.sleep(0.01)

        except Exception as e:
            print(f"Erreur lors de l'analyse de la page {url}: {str(e)}")

    return text_page_type, pdf_page_type

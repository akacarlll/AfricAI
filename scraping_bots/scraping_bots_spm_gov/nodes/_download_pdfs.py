import os
import requests

def download_pdfs(pdf_urls):
    """ Downloads all PDF files from the given URLs and saves them to a specified directory.

    Args: pdf_urls (list): List of URLs pointing to PDF files.

    Saves each PDF to the directory defined within the function. 
    """
    destination_folder = r"C:\Users\carlf\Documents\GitHub\LawIntelAfrica\data\01_raw\pdfs"
    if not os.path.exists(destination_folder):
        os.makedirs(destination_folder)

    for pdf_url in pdf_urls:
        try:
            pdf_name = pdf_url.split("/")[-1]
            destination_path = os.path.join(destination_folder, pdf_name)

            response = requests.get(pdf_url, stream=True)
            response.raise_for_status()

            with open(destination_path, 'wb') as pdf_file:
                for chunk in response.iter_content(chunk_size=8192):
                    pdf_file.write(chunk)

        except Exception as e:
            print(f"Erreur lors du téléchargement de {pdf_url}: {e}")
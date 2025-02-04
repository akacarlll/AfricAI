import os
import csv
import requests
from bs4 import BeautifulSoup
from urllib.parse import urlparse, unquote

def extract_text(urls):
    """
    Downloads the text from all <p> tags of the given pages and creates a file for each page.
    Uses the page title (<h2 class="main-title">) as the file name.

    Arguments:
    - urls (list): List of URLs of the pages containing text.
    """
    destination_folder = r"C:\Users\carlf\Documents\GitHub\LawIntelAfrica\data\01_raw\texts"
    os.makedirs(destination_folder, exist_ok=True)

    for url in urls:
        try:
            response = requests.get(url)
            response.raise_for_status()
            soup = BeautifulSoup(response.text, 'html.parser')

            title_element = soup.find('h2', class_='main-title')
            if title_element:
                title = title_element.get_text(strip=True)
                file_name = generate_file_name(title)
            else:
                file_name = "page_without_title"
            
            file_path = os.path.join(destination_folder, f"{file_name}.csv")

            paragraphs = soup.find_all('p')
            text = "\n".join(p.get_text(strip=True) for p in paragraphs)
            
            with open(file_path, mode='w', newline='', encoding='utf-8') as csv_file:
                writer = csv.writer(csv_file)
                writer.writerow(["URL", "Text"])
                writer.writerow([url, text])
            
            print(f"Text extracted and added to file: {file_path}")
        
        except Exception as e:
            print(f"Error processing {url}: {e}")

def generate_file_name(title):
    """
    Generates a file name from a page title, with intelligent truncation.

    If the full title exceeds 100 characters, it truncates at the last underscore
    before the length exceeds 100 characters.

    Arguments:
    - title (str): The page title.

    Returns:
    - str: The adapted file name.
    """
    cleaned_title = unquote(title).replace("/", "-").replace("\\", "-").replace("?", "-").replace("&", "-").replace(":", "-").replace(" ", "_")
    
    if len(cleaned_title) > 100:
        last_underscore = cleaned_title[:100].rfind("_")
        if last_underscore != -1:
            cleaned_title = cleaned_title[:last_underscore]
        else:
            cleaned_title = cleaned_title[:100]
    
    return cleaned_title

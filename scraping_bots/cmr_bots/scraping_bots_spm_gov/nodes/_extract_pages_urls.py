import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin


def extract_pages_urls(url):
    """
    Extracts all page URLs from a given source page.

    This function fetches the page content from the specified URL,
    parses it for certain structured elements, and collects the links.
    It handles cases where expected HTML tags or attributes might be missing.

    Args:
        url (str): URL of the source page to scrape.

    Returns:
        list: List of fully resolved URLs found on the page.
    """
    urls = []

    try:
        response = requests.get(url)
        soup = BeautifulSoup(response.text, "html.parser")

        rows = soup.find_all("div", class_="views-row")

        for row in rows:
            h3_tag = row.find("h3")
            if h3_tag:
                link = h3_tag.find("a")
                if link and "href" in link.attrs:
                    full_url = urljoin("https://www.spm.gov.cm", link["href"])
                    urls.append(full_url)

        return urls

    except Exception as e:
        print(f"Erreur lors de l'extraction des URLs: {str(e)}")
        return []

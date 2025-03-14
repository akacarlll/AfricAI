import requests
from bs4 import BeautifulSoup
import time
import random
from nodes import (
    extract_pages_urls,
    detect_page_type,
    extract_text,
    download_pdfs,
)


def cameroon_law_scraper():
    """
    Scrapes legal documentation from the Cameroon government website.

    This function iterates through multiple pages of the Cameroon government website's legal documentation section,
    extracting URLs, categorizing them into text-based pages and PDF download links, and then retrieving their content.
    It continues until it encounters a page indicating no further content, at which point it stops and prints summary details.

    Steps:
    - Builds the URL for the current page based on a base URL and pagination parameters.
    - Parses the page content to check for the presence of a "no content" message.
    - If content is available, extracts page URLs, categorizes them, and either downloads PDFs or retrieves textual content.
    - Repeats the process for the next page until no further content is available.

    No arguments or return values; all outputs are printed to the console or stored via external functions.
    """
    base_url = "https://www.spm.gov.cm/site/"
    page_param = "?q=fr/documentation/lois-et-r%C3%A8glements"
    page = 12

    while True:
        if page == 0:
            url = base_url + page_param
        else:
            url = base_url + page_param + f"&page={page}"

        response = requests.get(url)
        soup = BeautifulSoup(response.text, "html.parser")

        # Last page isn't empty but contains "Contenu en cours de préparation"
        empty_content = soup.find("div", class_="view-empty")
        if empty_content and "Contenu en cours de préparation" in empty_content.text:
            print(f"Dernière page trouvée: {page-1}")
            print(f"URL dernière page: {base_url + page-1}")
            print(f"URL première page: {base_url + page_param}")
            break

        urls_list = extract_pages_urls(url)

        text_page_list, pdf_page_list = detect_page_type(urls_list)

        extract_text(text_page_list)
        download_pdfs(pdf_page_list)

        print(f"Page {page} done")
        page += 1
        sleep_time = random.uniform(1, 3)
        print(f"Sleeping for {sleep_time} seconds")
        time.sleep(sleep_time)


if __name__ == "__main__":
    cameroon_law_scraper()

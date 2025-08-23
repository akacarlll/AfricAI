"""Module to Scrape data from benin laws"""

from urllib import response
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from selenium.common.exceptions import TimeoutException
import sys
import time
import os
import random
import requests
import logging
from urllib.parse import urljoin
import glob, shutil

logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)

src_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..")
sys.path.insert(0, src_path)

from scraping_bots.extras.scraping_function import generate_file_name


logger = logging.getLogger(__name__)
CATEGORY_MAP = {
    "loi": "loi",
    "docs": "decret",
    "ordonnance": "ordonnance",
    "accord": "accord",
    "decision": "decision",
}


class BeninLawsScraper:
    def __init__(self, category: str):
        self.base_url = "https://sgg.gouv.bj/recherche/?keywords=&begin=&end=&type="
        self.category = CATEGORY_MAP[category]
        self.url_to_target = f"{self.base_url}{self.category}"
        self.base_folder = (
            r"C:\Users\carlf\Documents\GitHub\AfricAI\data\01_raw\ben\pdfs"
        )

    def scrape_laws(self):
        page = 1
        driver = self.setup_webdriver(self.category)

        while True:
            driver.get(self.url_to_target + f"&offset={str(page)}")
            links_to_pdf_page = self.create_links_list(driver)
            logger.info(len(links_to_pdf_page))
            for link in links_to_pdf_page:
                driver.get(link)
                page_title = self.get_page_title(driver)
                file_name = generate_file_name(page_title)
                self.gather_downloadable_link(driver, file_name)

                file_downloaded_msg = f"Downloaded {file_name}"
                logger.info(file_downloaded_msg)

            page_downloaded_msg = (
                f"Page {page} done, {len(links_to_pdf_page)} {self.category} downloaded"
            )
            logger.info(page_downloaded_msg)
            page += 1

    def setup_webdriver(self, category: str):
        destination_folder = os.path.join(self.base_folder, category)
        os.makedirs(destination_folder, exist_ok=True)

        options = webdriver.ChromeOptions()
        options.add_argument("--start-maximized")
        options.add_argument("--blink-settings=imagesEnabled=false")
        options.add_argument("--headless=new")

        prefs = {
            "download.default_directory": destination_folder,  # where to save
            "download.prompt_for_download": False,  # no dialog
            "download.directory_upgrade": True,
            "plugins.always_open_pdf_externally": True,  # avoid Chrome's PDF viewer
        }
        options.add_experimental_option("prefs", prefs)

        return webdriver.Chrome(
            service=Service(ChromeDriverManager().install()), options=options
        )

    def create_links_list(self, driver) -> list[str]:

        elements = driver.find_elements("css selector", "a.doc-title.highlight")

        relative_links = [el.get_attribute("href") for el in elements]

        return relative_links

    def get_page_title(self, driver) -> str:
        """
        Récupère le titre de la loi (balise <h1 class="upper adapt white">).
        """
        element = driver.find_element("css selector", "h1.upper.adapt.white")
        return element.text.strip()

    def gather_downloadable_link(self, driver, file_name) -> str | None:
        """
        Get the single downloadable PDF link from the current law page.
        Returns None if not found.
        """
        download_button = driver.find_element(By.ID, "btnDownload")
        driver.execute_script("arguments[0].click();", download_button)

        time.sleep(3)  # wait for download to finish (or poll for .crdownload)
        latest_file = max(
            glob.glob(os.path.join(self.base_folder, self.category, "*")),
            key=os.path.getctime,
        )
        new_path = os.path.join(self.base_folder, self.category, f"{file_name}.pdf")
        shutil.move(latest_file, new_path)


list_of_category_to_scrape = ["loi", "docs", "ordonnance", "accord", "decision"]
for category in list_of_category_to_scrape:
    scraper = BeninLawsScraper(category=category)
    scraper.scrape_laws()

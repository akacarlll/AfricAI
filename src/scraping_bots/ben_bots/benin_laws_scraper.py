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
import json

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
    """Scrapes laws from the Benin government website by category."""

    def __init__(self, category: str):
        self.base_url = "https://sgg.gouv.bj/recherche/?keywords=&begin=&end=&type="
        self.category = CATEGORY_MAP[category]
        self.url_to_target = f"{self.base_url}{self.category}"
        self.base_folder = (
            r"C:\Users\carlf\Documents\GitHub\AfricAI\data\01_raw\ben\pdfs"
        )
        self.page_downloaded_file = "last_page_downloaded.json"

    def scrape_laws(self) -> None:
        """Scrapes all laws for the given category."""
        # page = self.load_last_page_downloaded()
        page = 14
        driver = self.setup_webdriver(self.category)

        while True:
            driver.get(f"{self.url_to_target}&offset={str(page)}")
            links_to_pdf_page = self.create_links_list(driver)
            logger.info(len(links_to_pdf_page))
            for link in links_to_pdf_page:
                try_downloaded_msg = f"Trying to download: {link}"
                logger.info(try_downloaded_msg)

                driver.get(link)
                page_title = self.get_page_title(driver)
                file_name = generate_file_name(page_title)
                self.download_file(driver, file_name)

                file_downloaded_msg = f"Downloaded {file_name}"
                logger.info(file_downloaded_msg)

            page_downloaded_msg = (
                f"Page {page} done, {len(links_to_pdf_page)} {self.category} downloaded"
            )
            logger.info(page_downloaded_msg)
            # self.save_last_page_downloaded(page)
            page += 1

    def setup_webdriver(self, category: str) -> webdriver.Chrome:
        """Sets up the Selenium WebDriver with download preferences.

        Args:
            category (str): The category to create the download folder for.

        Returns:
            WebDriver: The configured Chrome WebDriver instance.
        """
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

    def create_links_list(self, driver: webdriver.Chrome) -> list[str]:
        """Creates a list of links to law detail pages.

        Args:
            driver: The Selenium WebDriver instance.

        Returns:
            list[str]: A list of URLs.
        """
        elements = driver.find_elements("css selector", "a.doc-title.highlight")

        return [el.get_attribute("href") for el in elements]  # type: ignore

    def get_page_title(self, driver: webdriver.Chrome) -> str:
        """Gets the title of the law from the page.

        Args:
            driver: The Selenium WebDriver instance.

        Returns:
            str: The title of the law.
        """
        element = driver.find_element("css selector", "h1.upper.adapt.white")
        return element.text.strip()

    def download_file(self, driver: webdriver.Chrome, file_name: str) -> None:
        """Clicks the download button and renames the downloaded file.

        Args:
            driver: The Selenium WebDriver instance.
            file_name (str): The desired name for the downloaded file.

        Returns:
            None.
        """
        download_button = driver.find_element(By.ID, "btnDownload")
        driver.execute_script("arguments[0].click();", download_button)


        download_dir = os.path.join(self.base_folder, self.category)
        latest_file = self.wait_for_download(download_dir)

        new_path = os.path.join(download_dir, f"{file_name}.pdf")
        shutil.move(latest_file, new_path)

    def wait_for_download(self, download_dir: str, timeout: int = 60) -> str:
        """Waits for the latest Chrome download to finish and returns its path."""
        end_time = time.time() + timeout
        initial_files = set(glob.glob(os.path.join(download_dir, "*")))
    
        while time.time() < end_time:
            current_files = set(glob.glob(os.path.join(download_dir, "*")))
            new_files = current_files - initial_files
            
            # Check for completed downloads (no .crdownload extension)
            completed_files = [f for f in new_files if not f.endswith(".crdownload")]
            if completed_files:
                return max(completed_files, key=os.path.getctime)
            
            # Check if download is in progress
            in_progress = [f for f in new_files if f.endswith(".crdownload")]
            if in_progress:
                # Wait for the .crdownload file to disappear (download complete)
                crdownload_file = in_progress[0]
                while time.time() < end_time and os.path.exists(crdownload_file):
                    time.sleep(0.3)
                completed_file = crdownload_file.replace(".crdownload", "")
                if os.path.exists(completed_file):
                    return completed_file
            
            time.sleep(0.3)
        raise TimeoutError("Download did not finish in time.")

    def save_last_page_downloaded(self, page: int) -> None:
        """Saves the last page number downloaded to a text file.

        Args:
            page (int): The last page number downloaded.

        Returns:
            None.
        """
    
        if os.path.exists(self.page_downloaded_file):
            with open(self.page_downloaded_file, "r", encoding="utf-8") as f:
                data = json.load(f)
        else:
            data = {}
        data[self.category] = page

        with open(self.page_downloaded_file, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=4)

    def load_last_page_downloaded(self) -> int:
        """Loads the last page number downloaded for category 'ran' from a JSON file.
        
        Returns:
            int: The last page number downloaded, or 1 if the file/category doesn't exist.
        """
        self.page_downloaded_file = "last_page_downloaded.json"
        
        if os.path.exists(self.page_downloaded_file):
            with open(self.page_downloaded_file, "r", encoding="utf-8") as f:
                data = json.load(f)
                return data.get(self.category, 1)
        else:
            return 1

            



list_of_category_to_scrape = ["docs", "ordonnance", "accord", "decision"]


def main():
    """Main function to run the scraping process"""
    for category in list_of_category_to_scrape:
        scraper = BeninLawsScraper(category=category)
        scraper.scrape_laws()


if __name__ == "__main__":
    main()
"""
page_to_scrape = {docs: 33, loi: year 1998, ordonnance: 1, accord: 1, decision:1}
"""
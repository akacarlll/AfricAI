from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from selenium.common.exceptions import TimeoutException
import time
import os
import random
import os
from scraping_bots.cmr_bots.extras.scraping_function import (
    save_file,
    generate_file_name,
    get_page_title,
    categorize_file,
)
from .bot_settings import email, password
import re

data_to_scrape = {
    "cameroon_regulations": "https://www.juriafrica.com/lex/result/reglementation-cameroun.htm",
    "cameroon_supreme_court_cases": "https://www.juriafrica.com/lex/result/jurisprudence-cameroun-cour-supreme.htm",  # page 840
    "ccja_case_law": "https://www.juriafrica.com/lex/result/jurisprudence-ccja.htm",
    "ohada_case_law": "https://www.juriafrica.com/lex/result/jurisprudence-ohada.htm",
}


def scrape_juriafrica(email: str, password: str, pages_to_scrape: str):
    """
    Se connecte à Juriafrica, récupère les documents légaux et les enregistre sous forme de fichiers texte.

    Args:
        email (str): Adresse email pour la connexion.
        password (str): Mot de passe pour la connexion.
    """
    driver = setup_webdriver()
    page = 0
    base_url = data_to_scrape[pages_to_scrape]
    page_param = "?pager.offset="
    base_folder = (
        r"C:\Users\carlf\Documents\GitHub\LawIntelAfrica\data\01_raw\cmr\texts"
    )

    try:
        login_to_juriafrica(driver, email, password)
        driver.get("https://www.juriafrica.com/lex/")
        configure_search_settings(driver)
        os.makedirs(base_folder, exist_ok=True)

        while True:
            driver.get(base_url + page_param + str(page))
            valid_links = create_links_list(driver, pages_to_scrape)
            for link in valid_links:
                driver.get(link)
                if "regulations" in pages_to_scrape:
                    title_element, text_content = extract_regulation_content(driver)
                    title = title_element.strip()
                else:

                    title_element, text_content, metadata = extract_judgment_content(
                        driver
                    )
                    title = title_element.strip()
                title_on_page = get_page_title(title)

                file_name = generate_file_name(title_on_page)
                category = categorize_file(file_name)
                sub_folder = os.path.join(base_folder, category)
                os.makedirs(sub_folder, exist_ok=True)
                file_path = os.path.join(sub_folder, f"{file_name}.csv")

                save_file(
                    file_path=file_path,
                    url=link,
                    text=text_content,
                    title_on_page=title_on_page,
                    category=category,
                    metadata=metadata if "regulations" not in pages_to_scrape else None,
                )

                sleep_time = random.uniform(0.1, 0.2)
                time.sleep(sleep_time)
            print(f"Files downloaded on page {page}")
            page += 15
    except Exception as e:
        print(f"❌ Erreur : {e}")
    finally:
        print(f"Last visited page : {base_url + page_param + str(page)}")
        driver.quit()


def setup_webdriver():
    options = webdriver.ChromeOptions()
    options.add_argument("--start-maximized")
    options.add_argument("--blink-settings=imagesEnabled=false")
    options.add_argument("--headless=new")
    return webdriver.Chrome(
        service=Service(ChromeDriverManager().install()), options=options
    )


def login_to_juriafrica(driver, email: str, password: str):
    driver.get("https://www.juriafrica.com/lex/")
    WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, "//a[@data-target='#LogonModal']"))
    ).click()

    WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.NAME, "login")))
    driver.find_element(By.NAME, "login").send_keys(email)
    driver.find_element(By.NAME, "password").send_keys(password)
    driver.find_element(
        By.XPATH, "//button[@type='submit' and contains(text(), 'SE CONNECTER')]"
    ).click()

    time.sleep(3)
    print("🔓 Connexion réussie !")


def configure_search_settings(driver):
    try:
        WebDriverWait(driver, 5).until(
            EC.element_to_be_clickable((By.ID, "search-option"))
        ).click()
        print("✅ Bouton 'Paramétrer' cliqué.")

        chrono_button = WebDriverWait(driver, 5).until(
            EC.element_to_be_clickable(
                (By.XPATH, '//label[@class="btn btn-secondary"]')
            )
        )
        chrono_button.click()
        print("✅ Mode 'Anté-chronologique' activé.")
    except TimeoutException:
        print("⚠️ 'Paramétrer' ou 'Anté-chronologique' non trouvé.")


def create_links_list(driver, pages_to_scrape):
    document_links = driver.find_elements(
        By.CSS_SELECTOR, 'a[rel="bookmark"][href^="/lex/"]'
    )

    links = [link.get_attribute("href") for link in document_links]

    valid_links = [
        link
        for link in links
        if "/result/jocm.htm" not in link
        and "/result/juriscm.htm" not in link
        and "jurisohada.htm" not in link
    ]
    return valid_links


def extract_regulation_content(driver):
    title_element = (
        WebDriverWait(driver, 10)
        .until(EC.presence_of_element_located((By.CLASS_NAME, "titre")))
        .text
    )
    text_container = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.CLASS_NAME, "texte"))
    )

    text_body_element = text_container.find_element(By.CLASS_NAME, "texte-body")
    text_content = "\n".join(
        [p.text.strip() for p in text_body_element.find_elements(By.TAG_NAME, "p")]
    )
    text_content = f"{title_element}\n\n{text_content}"
    return title_element, text_content


def safe_find_text(driver, by, selector, default=""):
    """Returns the text of an element if it exists, else returns a default value."""
    try:
        return (
            WebDriverWait(driver, 5)
            .until(EC.presence_of_element_located((by, selector)))
            .text
        )
    except:
        return default


def extract_judgment_content(driver):
    text_container = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.CLASS_NAME, "uddoc"))
    )
    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, ".entete.jurisprudence"))
    )
    metadata = {
        "Court": safe_find_text(driver, By.CSS_SELECTOR, ".tribunal"),
        "Chamber": safe_find_text(driver, By.CSS_SELECTOR, ".chambre"),
        "Section": safe_find_text(driver, By.CSS_SELECTOR, ".section"),
        "Case": safe_find_text(driver, By.CSS_SELECTOR, ".dossier"),
        "Appeal": safe_find_text(driver, By.CSS_SELECTOR, ".pourvoi"),
        "Claimant": safe_find_text(driver, By.CSS_SELECTOR, ".demandeur"),
        "Against": safe_find_text(driver, By.CSS_SELECTOR, ".contre"),
        "Defendant": safe_find_text(driver, By.CSS_SELECTOR, ".defendeur"),
        "Judgment": safe_find_text(driver, By.CLASS_NAME, "arret"),
    }
    title_on_page = metadata["Judgment"]

    text_body_elements = text_container.find_elements(By.CSS_SELECTOR, ".decision p")
    text_content = "\n".join([p.text.strip() for p in text_body_elements])
    text_content = f"{title_on_page}\n\n{text_content}"

    return title_on_page, text_content, metadata


if __name__ == "__main__":
    scrape_juriafrica(email, password, "cameroon_supreme_court_cases")

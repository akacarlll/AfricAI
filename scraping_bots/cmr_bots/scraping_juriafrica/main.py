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
from scraping_bots.cmr_bots.extras.scraping_function import save_file, generate_file_name, get_page_title
from .bot_settings import email, password
def scrape_juriafrica(email: str, password: str):
    """
    Se connecte à Juriafrica, récupère les documents légaux et les enregistre sous forme de fichiers texte.
    
    Args:
        email (str): Adresse email pour la connexion.
        password (str): Mot de passe pour la connexion.
    """
    options = webdriver.ChromeOptions()
    options.add_argument("--start-maximized")
    options.add_argument("--blink-settings=imagesEnabled=false")
    options.add_argument("--headless=new")
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

    try:
        driver.get("https://www.juriafrica.com/lex/")
        WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//a[@data-target='#LogonModal']"))
        ).click()
        WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.NAME, "login")))
        driver.find_element(By.NAME, "login").send_keys(email)
        driver.find_element(By.NAME, "password").send_keys(password)
        driver.find_element(By.XPATH, "//button[@type='submit' and contains(text(), 'SE CONNECTER')]").click()
        time.sleep(3)
        print("🔓 Connexion réussie !")
        driver.get("https://www.juriafrica.com/lex/")
        print("📄 Sur la page de recherche de documents.")
        try:
            WebDriverWait(driver, 5).until(
                EC.element_to_be_clickable((By.ID, "search-option"))
            ).click()
            print("✅ Bouton 'Paramétrer' cliqué.")
            chrono_button = WebDriverWait(driver, 5).until(
                EC.element_to_be_clickable((By.XPATH, '//label[@class="btn btn-secondary"]'))
            )
            chrono_button.click()
            print("✅ Mode 'Anté-chronologique' activé.")
        except TimeoutException:
            print("⚠️ 'Paramétrer' ou 'Anté-chronologique' non trouvé.")
        base_url = "https://www.juriafrica.com/lex/result/reglementation-cameroun.htm"
        page_param = "?pager.offset="
        page = 2385
        base_folder = r"C:\Users\carlf\Documents\GitHub\LawIntelAfrica\data\01_raw\cmr\texts"
        os.makedirs(base_folder, exist_ok=True)
        while True:
            driver.get(base_url + page_param + str(page))
            document_links = driver.find_elements(By.CSS_SELECTOR, 'a[rel="bookmark"][href^="/lex/"]')
            print("Links found")
            
            links = [link.get_attribute("href") for link in document_links]
            valid_links = [link for link in links if "/result/jocm.htm" not in link]
            for link in valid_links:
                driver.get(link)
                
                title_element = WebDriverWait(driver, 10).until(
                    EC.presence_of_element_located((By.CLASS_NAME, "titre"))
                )
                title = title_element.text.strip()
                title_on_page = get_page_title(title)
                
                texte_container = WebDriverWait(driver, 10).until(
                    EC.presence_of_element_located((By.CLASS_NAME, "texte"))
                )
                text_body_element = texte_container.find_element(By.CLASS_NAME, "texte-body")
                text_content = "\n".join([p.text.strip() for p in text_body_element.find_elements(By.TAG_NAME, "p")])
                
                file_name = generate_file_name(title_on_page)
                category = "autres"  # Par défaut
                if "decret" in file_name.lower():
                    category = "decret"
                elif "arrete" in file_name.lower():
                    category = "arrete"
                elif "circulaire" in file_name.lower():
                    category = "circulaire"
                elif "loi" in file_name.lower():
                    category = "loi"

                sub_folder = os.path.join(base_folder, category)
                os.makedirs(sub_folder, exist_ok=True)  # Création du dossier si inexistant
            
                # Définition du chemin du fichier
                file_path = os.path.join(sub_folder, f"{file_name}.csv")
                    
                
                save_file(file_path,link, text_content, title_on_page )
                # print(f"✅ Texte sauvegardé : {file_path}")
                
                sleep_time = random.uniform(0.1,0.2)
                time.sleep(sleep_time)
            print(f"Files downloaded on page {page}")
            page += 15
    except Exception as e:
        print(f"❌ Erreur : {e}")
    finally:
        # print(f"Dernière page visité: {page} ")
        print(f"Dernière page avec URL des lois visité : {driver.get(base_url + page_param + str(page))}")
        # input("\n🔹 Appuie sur [Entrée] pour fermer le navigateur...")
        
        driver.quit()

# Exemple d'utilisation :
scrape_juriafrica(email, password)



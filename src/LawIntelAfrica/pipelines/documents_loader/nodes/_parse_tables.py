import pdfplumber
import pandas as pd
import os 

def detect_pages_with_tables(pdf_path: str):
    table_pages = []
    with pdfplumber.open(pdf_path) as pdf:
        for i, page in enumerate(pdf.pages):
            extracted_tables = page.extract_tables()
            if extracted_tables:  # Vérifie si un tableau est détecté
                table_pages.append(i + 1)  # On stocke le numéro de la page (commence à 1)
    
    return table_pages

# Exemple d'utilisation
pdf_path = r"C:\Users\carlf\Documents\GitHub\LawIntelAfrica\data\01_raw\cmr\code\CONSTITUTION_CAMEROUN.pdf"
pages_with_tables = detect_pages_with_tables(pdf_path)
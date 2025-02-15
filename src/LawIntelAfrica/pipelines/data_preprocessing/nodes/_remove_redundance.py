import pandas as pd
import re


def remove_redundance(df: pd.DataFrame):
    df = clean_ohada_text(df)
    df = clean_civil_code_text(df)
    df = clean_electoral_code(df)
    df = clean_tax_code(df)
    df = clean_codes(df)
    
    return df



def clean_ohada_text(df: pd.DataFrame) -> pd.DataFrame:
    """
    Remove OHADA header from text column when document_name is 'Acte_OHADA'.
    
    Args:
        df (pd.DataFrame): DataFrame with 'text' and 'document_name' columns
        
    Returns:
        pd.DataFrame: DataFrame with cleaned text
    """
    header = "ACTE UNIFORME REVISE RELATIF AU DROIT DES SOCIETES COMMERCIALES ET DU GROUPEMENT D'INTERET ECONOMIQUE Adopte le 30012014 a Ouagadougou (BURKINA FASO)"
    footer_pattern = r"page \d+ 209 http:www\.ohada\.comactes-uniformes-revises1299acte-uniforme-revise-relatif-au-droit-des-societes-commerciales-et-du-groupement-d-interet-economique\.html"

    
    mask = df['document_name'] == 'ACTE_OHADA'
    df.loc[mask, 'text'] = (df.loc[mask, 'text']
                           .str.replace(header, '', regex=False)
                           .str.replace(footer_pattern, '', regex=True))
    
    return df

def clean_civil_code_text(df: pd.DataFrame): 
    # Expression régulière pour capturer les motifs entre 'X.' et 'p.YY'
    pattern = r'''
    (?<!Art\.\s)       # Negative lookbehind pour exclure "Art. "
    \b\d+\.            # Chiffre suivi d'un point (ex: "2.")
    \s*                # Espaces optionnels
    (.*?)              # Contenu à supprimer (non gourmand)
    \s*p\.\s*\d+       # Référence de page (ex: "p.55" ou "p. 55")
    '''

    mask = df['document_name'] == "CODE_CIVIL"
    df.loc[mask, 'text'] = df.loc[mask, 'text'].str.replace(
        pattern,
        '',
        flags=re.VERBOSE | re.IGNORECASE | re.DOTALL,
        regex=True
    )

    return df


def clean_codes(df: pd.DataFrame) -> pd.DataFrame:
    """
    Cleans specific texts from the legal documents based on their document_name.

    Args:
        df (pd.DataFrame): DataFrame containing 'document_name' and 'text' columns.

    Returns:
        pd.DataFrame: Cleaned DataFrame.
    """
    patterns = {
        'CODE_MARCHE_PUBLIC': r"www.Droit-Afrique.com Cameroun Code des marches publics \d+",
        'CODE_PETROLIER': r"www.Droit-Afrique.com Cameroun Code petrolier \d+",
        'CODE_TRAVAIL': r"www.Droit-Afrique.com Cameroun Code du travail \d+"
    }
    
    for doc_name, pattern in patterns.items():
        mask = df['document_name'] == doc_name
        df.loc[mask, 'text'] = df.loc[mask, 'text'].str.replace(pattern, '', regex=True)

    return df



def clean_electoral_code(df: pd.DataFrame) -> pd.DataFrame:
    """
    Remove electoral code headers from the text column when document_name is 'CODE_ELECTORAL'.
    
    Args:
        df (pd.DataFrame): DataFrame with 'text' and 'document_name' columns.
        
    Returns:
        pd.DataFrame: DataFrame with cleaned text.
    """
    patterns = [
        r"Code electorale Fr v8 bis:Mise en page 1\s+\d{2}/\d{2}/\d{4}\s+\d{2}:\d{2}\s+Page \d+",
        r"Elections Cameroon - ELECAM"
    ]
    
    mask = df['document_name'] == "CODE_ELECTORAL"
    
    # Apply each pattern sequentially
    for pattern in patterns:
        df.loc[mask, 'text'] = df.loc[mask, 'text'].str.replace(pattern, "", regex=True)
    
    return df


def clean_tax_code(df: pd.DataFrame):
    """
    Remove electoral code header from text column when document_name is 'CODE_ELECTORAL'.
    
    Args:
        df (pd.DataFrame): DataFrame with 'text' and 'document_name' columns
        
    Returns:
        pd.DataFrame: DataFrame with cleaned text
    """
    pattern = r"Code General des Imports Edition officielle 2024 \d+"
    
    # Créer un masque pour sélectionner les lignes où 'document_name' est "CODE_ELECTORAL"
    mask = df['document_name'] == "CODE_GENERAL_IMPOTS"
    
    # Appliquer la regex uniquement sur les lignes correspondant au masque
    df.loc[mask, 'text'] = df.loc[mask, 'text'].str.replace(pattern, "", regex=True)
    
    return df

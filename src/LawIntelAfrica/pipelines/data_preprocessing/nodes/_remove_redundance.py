import pandas as pd
import re


def remove_redundance(df: pd.DataFrame) -> pd.DataFrame:
    """
    Remove redundant text from the DataFrame based on document types.

    Args:
        df (pd.DataFrame): DataFrame containing 'text' and 'page_title' columns.

    Returns:
        pd.DataFrame: Cleaned DataFrame.
    """
    df = clean_ohada_text(df)
    df = clean_civil_code_text(df)
    df = clean_electoral_code(df)
    df = clean_tax_code(df)
    df = clean_codes(df)

    return df


def clean_ohada_text(df: pd.DataFrame) -> pd.DataFrame:
    """
    Remove OHADA header from text column when page_title is 'Acte_OHADA'.

    Args:
        df (pd.DataFrame): DataFrame with 'text' and 'page_title' columns.

    Returns:
        pd.DataFrame: DataFrame with cleaned text.
    """
    header = "ACTE UNIFORME REVISE RELATIF AU DROIT DES SOCIETES COMMERCIALES ET DU GROUPEMENT D'INTERET ECONOMIQUE Adopte le 30012014 a Ouagadougou (BURKINA FASO)"
    footer_pattern = r"page \d+ 209 http:www\.ohada\.comactes-uniformes-revises1299acte-uniforme-revise-relatif-au-droit-des-societes-commerciales-et-du-groupement-d-interet-economique\.html"

    mask = df["page_title"] == "ACTE_OHADA"
    df.loc[mask, "text"] = (
        df.loc[mask, "text"]
        .str.replace(header, "", regex=False)
        .str.replace(footer_pattern, "", regex=True)
    )

    return df


def clean_civil_code_text(df: pd.DataFrame) -> pd.DataFrame:
    """
    Remove specific patterns from text column when page_title is 'CODE_CIVIL'.

    Args:
        df (pd.DataFrame): DataFrame with 'text' and 'page_title' columns.

    Returns:
        pd.DataFrame: DataFrame with cleaned text.
    """
    # Regular expression to capture patterns between 'X.' and 'p.YY'
    pattern = r"""
    (?<!Art\.\s)       # Negative lookbehind to exclude "Art. "
    \b\d+\.            # Digit followed by a dot (e.g., "2.")
    \s*                # Optional spaces
    (.*?)              # Content to remove (non-greedy)
    \s*p\.\s*\d+       # Page reference (e.g., "p.55" or "p. 55")
    """

    mask = df["page_title"] == "CODE_CIVIL"
    df.loc[mask, "text"] = df.loc[mask, "text"].str.replace(
        pattern, "", flags=re.VERBOSE | re.IGNORECASE | re.DOTALL, regex=True
    )

    return df


def clean_codes(df: pd.DataFrame) -> pd.DataFrame:
    """
    Cleans specific texts from the legal documents based on their page_title.

    Args:
        df (pd.DataFrame): DataFrame containing 'page_title' and 'text' columns.

    Returns:
        pd.DataFrame: Cleaned DataFrame.
    """
    patterns = {
        "CODE_MARCHE_PUBLIC": r"www.Droit-Afrique.com Cameroun Code des marches publics \d+",
        "CODE_PETROLIER": r"www.Droit-Afrique.com Cameroun Code petrolier \d+",
        "CODE_TRAVAIL": r"www.Droit-Afrique.com Cameroun Code du travail \d+",
    }

    for doc_name, pattern in patterns.items():
        mask = df["page_title"] == doc_name
        df.loc[mask, "text"] = df.loc[mask, "text"].str.replace(pattern, "", regex=True)

    return df


def clean_electoral_code(df: pd.DataFrame) -> pd.DataFrame:
    """
    Remove electoral code headers from the text column when page_title is 'CODE_ELECTORAL'.

    Args:
        df (pd.DataFrame): DataFrame with 'text' and 'page_title' columns.

    Returns:
        pd.DataFrame: DataFrame with cleaned text.
    """
    patterns = [
        r"Code electorale Fr v8 bis:Mise en page 1\s+\d{2}/\d{2}/\d{4}\s+\d{2}:\d{2}\s+Page \d+",
        r"Elections Cameroon - ELECAM",
    ]

    mask = df["page_title"] == "CODE_ELECTORAL"

    # Apply each pattern sequentially
    for pattern in patterns:
        df.loc[mask, "text"] = df.loc[mask, "text"].str.replace(pattern, "", regex=True)

    return df


def clean_tax_code(df: pd.DataFrame) -> pd.DataFrame:
    """
    Remove tax code header from text column when page_title is 'CODE_GENERAL_IMPOTS'.

    Args:
        df (pd.DataFrame): DataFrame with 'text' and 'page_title' columns.

    Returns:
        pd.DataFrame: DataFrame with cleaned text.
    """
    pattern = r"Code General des Imports Edition officielle 2024 \d+"

    # Create a mask to select rows where 'page_title' is "CODE_GENERAL_IMPOTS"
    mask = df["page_title"] == "CODE_GENERAL_IMPOTS"

    # Apply the regex only on the rows corresponding to the mask
    df.loc[mask, "text"] = df.loc[mask, "text"].str.replace(pattern, "", regex=True)

    return df

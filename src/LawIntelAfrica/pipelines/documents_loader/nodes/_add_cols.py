import pandas as pd
import re

def extract_metadata(df: pd.DataFrame) -> pd.DataFrame:
    """Extracts the columns from the line of the document and adds them to the DataFrame.

    This function extracts the columns from the line of the document and adds them to the DataFrame
    as separate columns.

    Args:
        df (pd.DataFrame): A DataFrame containing the documents.

    Returns:
        pd.DataFrame: A DataFrame containing the documents with the extracted columns.
    """
    
    df['page_title'] = df['source'].apply(
        extract_document_name
    )
    
    
    df.drop(columns=['source', "page"], inplace=True)
    
    return df

def extract_document_name(file_path):
    """
    Extracts the document name from the file path by splitting after the occurrence of a prefix (code, arrete, decret, etc.).

    Args:
        file_path (str): The full path of the file.

    Returns:
        str: The document name extracted from the file path.
    """
    pattern = r"(code|arrete|decret|loi|autres|circulaire)\\([^\\]+)\.pdf"

    match = re.search(pattern, file_path, re.IGNORECASE)
    if match:
        return match.group(2)  # Prend la partie après le préfixe et avant .pdf
    return None
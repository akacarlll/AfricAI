import pandas as pd
import re
import os

def extract_metadata(df: pd.DataFrame) -> pd.DataFrame:
    """Extracts the columns from the line of the document and adds them to the DataFrame.

    This function extracts the columns from the line of the document and adds them to the DataFrame
    as separate columns.

    Args:
        df (pd.DataFrame): A DataFrame containing the documents.

    Returns:
        pd.DataFrame: A DataFrame containing the documents with the extracted columns.
    """

    df["page_title"] = df.apply(
        lambda row: (
            extract_document_name(row["source"])
            if pd.isna(row.get("page_title"))
            else row["page_title"]
        ),
        axis=1,
    )
    df["category"] = df.apply(
        lambda row: (
            extract_category(row["page_title"])
            if pd.isna(row.get("category"))
            else row["category"]
        ),
        axis=1,
    )
    # TODO: Add a column for metadata extraction
    return df


def extract_document_name(file_path):
    """
    Extracts the document name from the file path using os.path functions.
    
    Args:
        file_path (str): The full path of the file.
        
    Returns:
        str: The document name (filename without extension).
    """
    # Get just the filename without the directory
    filename = os.path.basename(file_path)
    
    # Remove the extension
    document_name = os.path.splitext(filename)[0]
    
    return document_name


def extract_category(page_title):
    """
    Extracts the category from the page title by checking for specific keywords.

    Args:
        page_title (str): The title of the page.

    Returns:
        str: The category extracted from the page title.
    """
    keywords = ["code", "arrete", "decret", "loi", "autres", "circulaire"]
    for keyword in keywords:
        if keyword in page_title.lower():
            return keyword
    return "autres"

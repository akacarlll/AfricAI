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
    df.drop(
        columns=[
            "source",
            "page",
            "producer",
            "creator",
            "creationdate",
            "keywords",
            "moddate",
            "author",
            "total_pages",
        ],
        inplace=True,
    )
    # TODO: Add a column for metadata extraction
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

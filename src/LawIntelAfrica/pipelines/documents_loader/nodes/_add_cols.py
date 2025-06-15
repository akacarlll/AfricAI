import pandas as pd
import re
import os
from langdetect import detect, LangDetectException
import ast
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
    df["year"] = df["page_title"].apply(extract_year)
    df["_temp_page_content_year"] = df["page_content"].apply(extract_year)
    consolidated_content_years = df.groupby("page_title")["_temp_page_content_year"].transform(lambda x: x.max() if x.dropna().any() else None)
    df["year_maybe"] = df.apply(
        lambda row: (
            row["year"]
            if row["year"] is not None
            else consolidated_content_years.loc[row.name]
        ),
        axis=1
    )

    df = df.drop(columns=["_temp_page_content_year"])
    df["country"] = df["source"].apply(extract_country_from_source)
    df["language"] = df["page_content"].apply(lambda x: detect_language(str(x)[:200]) if pd.notna(x) else "Unknown")

    parsed_metadata = df["metadata"].apply(parse_metadata_string)
    all_metadata_keys = set()
    for d in parsed_metadata:
        if isinstance(d, dict):
            all_metadata_keys.update(d.keys())

    for key in all_metadata_keys:
        df[key] = parsed_metadata.apply(lambda x: x.get(key) if isinstance(x, dict) else None)

    # TODO: Add a column for metadata extraction
    df.drop(columns=["_temp_page_content_year"], inplace=True)
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

def extract_year(text: str) -> int | None:
    """
    Extracts a 4-digit year from a given text.

    Args:
        text (str): The text from which to extract the year (e.g., page title or page content).

    Returns:
        int | None: The largest valid year (between 1960 and 2030) found in the text
                    as an integer, or None if no valid year is found.
    """
    if not isinstance(text, str):
        return None

    potential_years_str = re.findall(r"\b(\d{4})\b", text)

    valid_years = []
    for year_str in potential_years_str:
        try:
            year = int(year_str)
            if 1940 <= year <= 2030:
                valid_years.append(year)
        except ValueError:
            continue

    if not valid_years:
        return None
    elif len(valid_years) > 1:
        print(f"DEBUG: Multiple valid years found in "{text[:50]}...": {valid_years}. Returning the largest: {max(valid_years)}.")
        return max(valid_years)
    else:
        return valid_years[0]
def extract_country_from_source(source_path: str) -> str | None:
    """
    Extracts a country name from a given source path based on specific codes.

    Args:
        source_path (str): The document"s source path.

    Returns:
        str | None: The full country name ("Cameroon", "Benin", "Côte D\"Ivoire"),
                    or None if no recognized code is found.
    """
    if not isinstance(source_path, str):
        return None

    source_path_lower = source_path.lower()

    if "cmr" in source_path_lower:
        return "Cameroon"
    elif "ben" in source_path_lower:
        return "Benin"
    elif "ci" in source_path_lower:
        return "Côte D'Ivoire"
    else:
        return None

def detect_language(text: str) -> str:
    """
    Detects the language of the given text using the 'langdetect' library.

    Args:
        text (str): The text snippet (e.g., first 200 characters of page_content).

    Returns:
        str: The detected language code (e.g., 'en', 'fr') or 'Unknown' if detection fails.
    """
    if not isinstance(text, str) or not text.strip():
        return "Unknown"

    try:
        return detect(text)
    except LangDetectException:
        return "Unknown"

def parse_metadata_string(metadata_str: str) -> dict:
    """
    Safely parses a string representation of a dictionary into a dictionary.

    Args:
        metadata_str (str): The string representation of a dictionary.

    Returns:
        dict: The parsed dictionary, or an empty dictionary if parsing fails or input is invalid.
    """
    if not isinstance(metadata_str, str) or not metadata_str.strip():
        return {}
    try:

        return ast.literal_eval(metadata_str)
    except (ValueError, SyntaxError, TypeError):
        print(f"WARNING: Could not parse metadata string: '{metadata_str}'. Returning empty dict.")
        return {}
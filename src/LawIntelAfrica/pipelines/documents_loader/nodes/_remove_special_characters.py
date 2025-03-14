import pandas as pd
import unicodedata
import chardet
import re


def remove_characters(df: pd.DataFrame) -> pd.DataFrame:
    """Removes special characters from the text.

    This function removes special characters from the text.

    Args:
        df (pd.DataFrame): A DataFrame containing the text.

    Returns:
        pd.DataFrame: A DataFrame containing the text with the special characters removed.
    """

    df["text"] = df["text"].apply(remove_accents_and_special_chars)
    df["page_title"] = df["page_title"].apply(remove_accents_and_special_chars)

    df["text"] = df["text"].str.replace(
        r"[^a-zA-Z0-9\s.,!?'\"\-:;(){}[\]]", "", regex=True
    )
    return df


def remove_accents_and_special_chars(text: str) -> str:
    """
    Removes accents and special characters from a given text.

    Args:
        text (str): The input text containing accents and/or special characters.

    Returns:
        str: The cleaned text with accents and special characters removed.
    """
    normalized = unicodedata.normalize("NFKD", text)
    # Remove non-ASCII characters
    ascii_text = normalized.encode("ASCII", "ignore").decode("ASCII")
    return ascii_text

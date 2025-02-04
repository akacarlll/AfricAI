import pandas as pd 
import unicodedata

def remove_characters(df: pd.DataFrame) -> pd.DataFrame:
    """Removes special characters from the text.

    This function removes special characters from the text.

    Args:
        df (pd.DataFrame): A DataFrame containing the text.

    Returns:
        pd.DataFrame: A DataFrame containing the text with the special characters removed.
    """
    
    df["text"] = df["text"].apply(remove_accents_and_special_chars)
    df["text"] = df["text"].str.replace(r"[^a-zA-Z0-9\s.,!?'\"\-:;(){}[\]]", "", regex=True)
    return df

def remove_accents_and_special_chars(text):
    text = unicodedata.normalize("NFKD", text).encode("ascii", "ignore").decode("utf-8")
    return text

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
    df["text"] = df["text"].str.replace(r"[^a-zA-Z0-9\s.,!?'\"\-:;(){}[\]]", "", regex=True)
    df["text"] =  df["text"].str.replace(r"[\x80-\xFF]", "",regex=True)
    #Hard-coded because this binary cause encoding issues
    df["text"] = df["text"].str.replace('\xdb', '°', regex=False)
    
    return df

def remove_accents_and_special_chars(text):
    """_summary_

    Args:
        text (_type_): _description_

    Returns:
        _type_: _description_
    """
    if isinstance(text, bytes):
        detected_encoding = chardet.detect(text)["encoding"]
        print(f"Detected encoding: {detected_encoding}")
        if not detected_encoding:
            detected_encoding = "utf-8"
        
        text = text.decode(detected_encoding, errors="ignore")
            
    normalized = unicodedata.normalize('NFKD', text)
    # Remove non-ASCII characters
    ascii_text = normalized.encode('ASCII', 'ignore').decode('ASCII')
    return ascii_text

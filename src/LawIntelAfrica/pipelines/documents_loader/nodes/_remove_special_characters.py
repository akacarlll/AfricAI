import pandas as pd
import unicodedata
from pandas.api.types import is_string_dtype
import unicodedata


def remove_characters(df: pd.DataFrame) -> pd.DataFrame:
    """Removes special characters from the text.

    This function removes special characters from the text.

    Args:
        df (pd.DataFrame): A DataFrame containing the text.

    Returns:
        pd.DataFrame: A DataFrame containing the text with the special characters removed.
    """
    find_unicode_chars(df)
    df = fully_clean_dataframe(df)
    return df.fillna("")


def find_unicode_chars(df):
    for col in df.columns:
        if df[col].dtype == object:
            mask = df[col].astype(str).apply(lambda x: any(ord(c) > 127 for c in x))
            if mask.any():
                print(f"Problem in column: {col}")
                print(df.loc[mask, col])


def fully_clean_dataframe(df: pd.DataFrame) -> pd.DataFrame:
    def clean_value(val):
        if not isinstance(val, str):
            return str(val)
        val = unicodedata.normalize("NFKD", val)
        val = val.encode("ascii", "ignore").decode("ascii")
        val = val.replace("\u2008", " ")
        return val

    for col in df.columns:
        if is_string_dtype(df[col]) or df[col].dtype == object:
            df[col] = df[col].fillna("").astype(str).map(clean_value)
    return df

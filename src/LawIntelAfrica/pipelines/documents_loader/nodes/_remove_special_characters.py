import logging
import pandas as pd
import unicodedata
from pandas.api.types import is_string_dtype
from typing import Any

logger = logging.getLogger(__name__)


def remove_characters(df: pd.DataFrame) -> pd.DataFrame:
    """
    Remove special characters from text columns in a DataFrame.

    Args:
        df (pd.DataFrame): Input DataFrame containing text columns to clean.

    Returns:
        pd.DataFrame: DataFrame with special characters removed from text columns and NaN values replaced with empty strings.
    """
    find_unicode_chars(df)
    df = fully_clean_dataframe(df)
    return df.fillna("")


def find_unicode_chars(df: pd.DataFrame) -> None:
    """
    Identify and log columns in a DataFrame containing non-ASCII characters.

    Args:
        df (pd.DataFrame): Input DataFrame to check for non-ASCII characters.

    Returns:
        None
    """
    for col in df.columns:
        if df[col].dtype == object or is_string_dtype(df[col]):
            mask = df[col].astype(str).apply(lambda x: any(ord(c) > 127 for c in x))
            if mask.any():
                problem_message = f"Problem in column: {col}\n{df.loc[mask, col]}"
                logger.info(problem_message)


def fully_clean_dataframe(df: pd.DataFrame) -> pd.DataFrame:
    """
    Clean text columns in a DataFrame by normalizing Unicode and removing non-ASCII characters.

    Args:
        df (pd.DataFrame): Input DataFrame with text columns to clean.

    Returns:
        pd.DataFrame: DataFrame with text columns cleaned of special characters.
    """

    def clean_value(val: Any) -> str:
        """
        Clean a single value by normalizing Unicode and removing non-ASCII characters.

        Args:
            val (Any): Input value to clean.

        Returns:
            str: Cleaned string value.
        """
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

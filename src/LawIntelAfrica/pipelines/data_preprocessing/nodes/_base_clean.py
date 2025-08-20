"""This module contains the functions to clean text data in a DataFrame."""

import pandas as pd
import re
import logging 

logger = logging.getLogger(__name__)

def clean_text(df: pd.DataFrame) -> pd.DataFrame:
    """
    Cleans the text data in the DataFrame

    Args:
        df (pd.DataFrame): DataFrame containing the page_content column.

    Returns:
        pd.DataFrame: A DataFrame with the page_column cleaned.
    """
    df["page_content"] = df["page_content"].astype(str).apply(lambda x: re.sub(r"\r", " ", x))
    df["page_content"] = df["page_content"].apply(lambda x: re.sub(r"\s+", " ", x))
    df["page_content"] = df["page_content"].apply(
        lambda x: re.sub(r"[\.-]{3,}", "", x)
    )  # Suppression des longues séquences de . et -
    df["page_content"] = df["page_content"].apply(lambda x: re.sub(r"\n\s*\n", "\n", x))
    df["page_content"] = df["page_content"].apply(lambda x: x.strip())

    number_of_docs_before_drop_na = len(df["page_title"].unique())
    df.dropna(subset=["page_content"], inplace=True)
    number_of_docs_after_drop_na = len(df["page_title"].unique())

    number_of_docs_dropped_msg = f"Number of documents deleted because of missing text: {number_of_docs_before_drop_na - number_of_docs_after_drop_na}"
    logger.info(number_of_docs_dropped_msg)
        
    return df

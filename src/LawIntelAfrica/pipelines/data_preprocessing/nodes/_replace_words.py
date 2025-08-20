import pandas as pd
import re


def replace_words(df: pd.DataFrame) -> pd.DataFrame:
    """Replace specific words in the DataFrame.

    Args:
        df (pd.DataFrame): DataFrame containing page_content and page_title columns.

    Returns:
        (pd.DataFrame): DataFrame with replaced words.
    """
    df["page_content"] = (
        df["page_content"]
        .astype(str)
        .apply(lambda x: re.sub(r"\bArt\.\b", "Article", x))
    )
    return df

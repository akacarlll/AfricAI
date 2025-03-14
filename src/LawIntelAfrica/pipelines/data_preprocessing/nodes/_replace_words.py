import pandas as pd
import re


def replace_words(df: pd.DataFrame):
    if "text" in df.columns:
        df["text"] = (
            df["text"].astype(str).apply(lambda x: re.sub(r"\bArt\.\b", "Article", x))
        )
    else:
        raise KeyError("Column 'text' not found in DataFrame")
    return df

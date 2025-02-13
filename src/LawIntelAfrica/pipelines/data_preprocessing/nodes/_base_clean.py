import pandas as pd
import re


def clean_text(df: pd.DataFrame) -> pd.DataFrame:
    if 'text' in df.columns:
        df['text'] = df['text'].astype(str).apply(lambda x: re.sub(r'\r\n', ' ', x))
        df['text'] = df['text'].apply(lambda x: re.sub(r'\s+', ' ', x))
        df['text'] = df['text'].apply(lambda x: re.sub(r'[\.-]{3,}', '', x))  # Suppression des longues séquences de . et -
        df['text'] = df['text'].apply(lambda x: re.sub(r'\n\s*\n', '\n', x))
        df['text'] = df['text'].apply(lambda x: x.strip())
    else:
        raise KeyError("Column 'text' not found in DataFrame")
    return df

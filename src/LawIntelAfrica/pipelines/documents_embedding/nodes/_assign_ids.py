import pandas as pd


def assign_unique_ids(df: pd.DataFrame) -> pd.DataFrame:
    """
    Assigns a unique ID to each chunk based on document name, page number, and chunk index.

    Args:
        df (pd.DataFrame): DataFrame with 'document_name', 'page', and text chunks.

    Returns:
        pd.DataFrame: Updated DataFrame with a new 'chunk_id' column.
    """
    df = df.copy()  # Avoid modifying original DataFrame

    df["chunk_index"] = df.groupby(
        ["document_name", "page_label"]
    ).cumcount()  # Create chunk index per page
    df["chunk_id"] = (
        df["document_name"]
        + ":"
        + df["page_label"].astype(str)
        + ":"
        + df["chunk_index"].astype(str)
    )

    return df.drop(columns=["chunk_index"])

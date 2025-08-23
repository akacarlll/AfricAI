import pandas as pd


def merge_document_in_df(cleaned_legal_documents: pd.DataFrame) -> pd.DataFrame:
    """
    Merges the 'page_content' and 'page_title' columns into a single DataFrame.

    Args:
        cleaned_legal_documents (pd.DataFrame): DataFrame containing 'page_content' and 'page_title'.

    Returns:
        pd.DataFrame: DataFrame with merged content.
    """
    aggregated_df = (
        cleaned_legal_documents.groupby("page_title")
        .agg(
            {
                "page_content": lambda x: "\n".join(x),
                **{
                    col: "first"
                    for col in cleaned_legal_documents.columns
                    if col not in ["page_title", "page_content"]
                },
            }
        )
        .reset_index()
    )
    return aggregated_df[aggregated_df["file_type"] == "csv"]

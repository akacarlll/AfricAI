import pandas as pd


def split_data(df: pd.DataFrame, split: bool) -> dict:
    """
    Splits the DataFrame based on the 'category' column if split is True.
    If split is False, returns the original DataFrame.

    Args:
        df (pd.DataFrame): The DataFrame to be split.
        split (bool): Whether to split the DataFrame or not.

    Returns:
        dict: A dictionary of DataFrames split by category if split is True,
              otherwise the original DataFrame.
    """
    if not split:
        return {"original": df}

    # Split the DataFrame based on the 'category' column
    split_dfs = {category: df_group for category, df_group in df.groupby("category")}

    return split_dfs

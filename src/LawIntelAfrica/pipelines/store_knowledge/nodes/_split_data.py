import pandas as pd

def split_data(df: pd.DataFrame, split_params: dict) -> dict[str, pd.DataFrame]:
    """
    Splits the DataFrame based on the 'category' column if split is True.
    If split is False, returns the original DataFrame.

    Args:
        df (pd.DataFrame): The DataFrame to be split.
        split_params (dict): A dictionary containing split parameters.

    Returns:
        dict: A dictionary of DataFrames split by category if split is True,
              otherwise the original DataFrame.
    """
    split = split_params["split"]
    
    if not split:
        return {"original": df}

    split_dfs = {str(category): df_group for category, df_group in df.groupby("category")}

    return split_dfs

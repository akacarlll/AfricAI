import pandas as pd


def split_data(df: pd.DataFrame) -> dict[str, pd.DataFrame]:
    """
    Splits the DataFrame based on the 'category' column.

    Args:
        df (pd.DataFrame): The DataFrame to be split.

    Returns:
        dict: A dictionary of DataFrames split by category.
    """

    return {
        str(category): df_group for category, df_group in df.groupby("category")
    }


"""This module is used to filter the dataset to be loaded in the vector stores.
We do this so it can be uploaded on github (Max size = 100Mb)"""

import pandas as pd


def filter_on_year(chunked_dataframe: pd.DataFrame, split_params: dict) -> pd.DataFrame:
    """
    Filter the dataframe based on the years to keep specified in split_params.
    Args:
        chunked_dataframe (pd.DataFrame): The dataframe to filter.
        split_params (dict): The parameters used for filtering.
    Returns:
        pd.DataFrame: The filtered dataframe.
    """
    if "years_to_keep" not in split_params:
        return chunked_dataframe

    years_to_keep = split_params["years_to_keep"]
    filtered_dataframe = chunked_dataframe[chunked_dataframe["year"].isin(years_to_keep)]
    return filtered_dataframe

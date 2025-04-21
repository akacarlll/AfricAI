import pandas as pd
def verify_columns(df: pd.DataFrame, expected_columns: list):
    """
    Verifies that the DataFrame contains exactly the expected columns.
    
    Args:
    -----------
    df (pd.DataFrame): The DataFrame to check
    expected_columns (list) : Column names that should be in the DataFrame
    
    Raises:
    -------
    ValueError
        If there are missing or extra columns, with details about which specific
        columns are missing or extra

    """
    actual_columns = set(df.columns)
    expected_column_set = set(expected_columns)

    if actual_columns != expected_column_set:

        missing_columns = expected_column_set - actual_columns
        extra_columns = actual_columns - expected_column_set
        error_message = "DataFrame columns do not match expected columns.\n"
        
        if missing_columns:
            error_message += f"Missing columns: {sorted(list(missing_columns))}\n"
        
        if extra_columns:
            error_message += f"Extra columns: {sorted(list(extra_columns))}"
        
        raise ValueError(error_message)
    
import pandas as pd 
def cleaning_text(df: pd.DataFrame) -> pd.DataFrame:
    """Cleans the text by removing special characters and accents.
    
    This function cleans the text by removing special characters and accents.
    
    Args:
        df (pd.DataFrame): A DataFrame containing the text.
        
    Returns:
        pd.DataFrame: A DataFrame containing the cleaned text.
    """
    
    df["text"] = df["text"].str.replace(r'[\r\n,]', ' ', regex=True)
    return df
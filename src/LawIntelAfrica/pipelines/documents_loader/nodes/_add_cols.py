import pandas as pd

def extract_metadata(df: pd.DataFrame) -> pd.DataFrame:
    """Extracts the columns from the line of the document and adds them to the DataFrame.

    This function extracts the columns from the line of the document and adds them to the DataFrame
    as separate columns.

    Args:
        df (pd.DataFrame): A DataFrame containing the documents.

    Returns:
        pd.DataFrame: A DataFrame containing the documents with the extracted columns.
    """
    
    df['document_name'] = df['source'].apply(
        lambda x: x.split('01_raw\\')[1].split('.')[0]
    )
    
    
    df.drop(columns=['source', "page"], inplace=True)
    
    return df
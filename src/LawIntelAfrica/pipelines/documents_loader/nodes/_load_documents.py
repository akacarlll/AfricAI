from langchain_community.document_loaders import PyPDFDirectoryLoader
import pandas as pd 


def load_documents(data_path:str)-> pd.DataFrame:
    """Loads documents from the specified directory and returns them as a Pandas DataFrame.

    This function uses PyPDFDirectoryLoader to load documents from the DATA_PATH directory
    and converts them into a Pandas DataFrame for further processing.

    Returns:
        pd.DataFrame: A DataFrame containing the loaded documents.
    """
    document_loader = PyPDFDirectoryLoader(data_path)
    return document_loader.load()

import chromadb
import pandas as pd
import os
from chromadb.utils import embedding_functions
from typing import Any, Union


def store_in_chroma(data: Union[pd.DataFrame, dict], chroma_params: dict):
    """
    Store embeddings and metadata in ChromaDB.

    Args:
        data (Union[pd.DataFrame, dict]): DataFrame with 'text', 'embedding', 'page_label', 'document_name', 'chunk_id',
                                          or a dictionary of DataFrames.
        chroma_params (dict): ChromaDB parameters from Kedro settings.

    Returns:
        str: Confirmation message.
    """

    if isinstance(data, pd.DataFrame):
        store_df_in_chroma(
            data, chroma_params["collection_name"], chroma_params["persist_directory"]
        )
    elif isinstance(data, dict):
        for category, df in data.items():
            category_folder = os.path.join(chroma_params["persist_directory"], category)
            os.makedirs(category_folder, exist_ok=True)
            store_df_in_chroma(
                df, f"{chroma_params['collection_name']}_{category}", category_folder
            )
    else:
        raise ValueError(
            "Data must be a pandas DataFrame or a dictionary of DataFrames."
        )

    return "Data successfully added to ChromaDB."


def store_df_in_chroma(df: pd.DataFrame, collection_name: str, persist_directory: str):
    # Initialize ChromaDB
    client = chromadb.PersistentClient(path=persist_directory)

    # Create or get the collection
    collection = client.get_or_create_collection(name=collection_name)

    # Prepare data for insertion
    ids = df["chunk_id"].astype(str).tolist()  # Ensure chunk_id is a string
    embeddings = df["embedding"].tolist()
    metadatas = df.drop(columns=["embedding"]).to_dict(orient="records")

    # Add data to ChromaDB
    collection.add(ids=ids, embeddings=embeddings, metadatas=metadatas)

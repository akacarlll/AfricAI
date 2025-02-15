import chromadb
import pandas as pd
from chromadb.utils import embedding_functions

def store_in_chroma(df: pd.DataFrame, chroma_params: dict):
    """
    Store embeddings and metadata in ChromaDB.

    Args:
        df (pd.DataFrame): DataFrame with 'text', 'embedding', 'page_label', 'document_name', 'chunk_id'.
        chroma_params (dict): ChromaDB parameters from Kedro settings.

    Returns:
        str: Confirmation message.
    """
    
    # Initialize ChromaDB
    client = chromadb.PersistentClient(path=chroma_params["persist_directory"])

    # Create or get the collection
    collection = client.get_or_create_collection(name=chroma_params["collection_name"])

    # Prepare data for insertion
    ids = df["chunk_id"].astype(str).tolist()  # Ensure chunk_id is a string
    embeddings = df["embedding"].tolist()
    metadatas = df.drop(columns=["embedding"]).to_dict(orient="records")

    # Add data to ChromaDB
    collection.add(
        ids=ids,
        embeddings=embeddings,
        metadatas=metadatas
    )


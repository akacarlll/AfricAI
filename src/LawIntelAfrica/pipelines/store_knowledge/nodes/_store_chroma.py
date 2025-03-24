import chromadb
import pandas as pd
import os
from chromadb.utils import embedding_functions
from typing import Any, Union, List, Dict, Optional
from tqdm import tqdm
import numpy as np


def store_in_chroma(data: Union[pd.DataFrame, dict], chroma_params: dict):
    """
    Store embeddings and metadata in ChromaDB.

    Args:
        data (Union[pd.DataFrame, dict]): DataFrame with 'chunk_text', 'embedding', 'page_label', 'page_title', 'chunk_id',
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


def store_df_in_chroma(
    df: pd.DataFrame,
    collection_name: str,
    persist_directory: str,
    batch_size: int = 100,
):
    """
    Store a DataFrame in ChromaDB with proper document storage and metadata.

    Args:
        df (pd.DataFrame): DataFrame containing text chunks and embeddings
        collection_name (str): Name for the ChromaDB collection
        persist_directory (str): Directory to store the ChromaDB database
        batch_size (int): Number of documents to add in each batch for performance

    Returns:
        chromadb.Collection: The ChromaDB collection object
    """
    # Initialize ChromaDB
    client = chromadb.PersistentClient(path=persist_directory)

    # Create or get the collection
    collection = client.get_or_create_collection(name=collection_name)

    # Ensure required columns exist
    required_columns = ["chunk_text", "chunk_id", "embedding"]
    for col in required_columns:
        if col not in df.columns:
            raise ValueError(f"Required column '{col}' not found in DataFrame")

    # Process in batches for better performance and memory usage
    total_records = len(df)
    batches = range(0, total_records, batch_size)

    for i in tqdm(batches, desc=f"Adding data to {collection_name}"):
        batch_df = df.iloc[i : min(i + batch_size, total_records)]

        # Prepare data for insertion - explicit naming of all components
        ids = batch_df["chunk_id"].astype(str).tolist()
        embeddings = batch_df["embedding"].tolist()
        documents = batch_df["chunk_text"].tolist()

        # Create proper metadata dictionary without duplicating text and embeddings
        metadatas = []
        for _, row in batch_df.iterrows():
            metadata = {}

            # Add all columns except text and embedding to metadata
            for col in batch_df.columns:
                if col not in ["chunk_text", "embedding", "chunk_id"]:
                    # Handle potential None values
                    if pd.notna(row[col]):
                        metadata[col] = row[col]

            metadatas.append(metadata)

        # Add data to ChromaDB with all components explicitly specified
        collection.add(
            ids=ids,
            embeddings=embeddings,
            documents=documents,  # This is the key change - explicitly storing document text
            metadatas=metadatas,
        )

    # Verify collection content
    count = collection.count()
    print(
        f"Successfully added {count} documents to ChromaDB collection '{collection_name}'"
    )

    return collection

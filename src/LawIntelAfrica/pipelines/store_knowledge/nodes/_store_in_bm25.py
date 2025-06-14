
import os
import pickle
from typing import Dict
import pandas as pd
from langchain_community.retrievers import BM25Retriever
from langchain.schema import Document
from LawIntelAfrica.utils.data_transformation._df_to_documents import df_to_documents


def create_bm25_stores(
    dataframes_dict: Dict[str, pd.DataFrame],
    output_dir: str = "./vector_stores/bm25_stores",
    chunk_text_column: str = "page_content"
) -> None:
    """
    Create BM25 stores from a dictionary of dataframes using LangChain documents.
    
    Args:
        dataframes_dict: Dict with category names as keys and dataframes as values
        output_dir: Directory to save the BM25 store files
        chunk_text_column: Name of the column containing text to embed
    """
    
    os.makedirs(output_dir, exist_ok=True)
    print("Creating BM25 stores...")
    bm25_stores = {}
    
    for category, df in dataframes_dict.items():
        print(f"Processing category: {category}")
        if chunk_text_column not in df.columns:
            print(f"Warning: '{chunk_text_column}' column not found in {category} dataframe. Skipping.")
            continue
            
        documents = df_to_documents(df, chunk_text_column, category)
        print(f"Creating BM25 index for {len(documents)} documents in {category}")
        
        bm25_retriever = BM25Retriever.from_documents(documents)
        
        store_path = os.path.join(output_dir, f"{category}.pkl")
        with open(store_path, 'wb') as f:
            pickle.dump(bm25_retriever, f)
        
        bm25_stores[category] = bm25_retriever
        
        print(f"✅ Successfully created BM25 store for {category}")
        print(f"   - Store path: {store_path}")
        print(f"   - Documents: {len(documents)}")
        print()
    
    print("🎉 All BM25 stores created successfully!")
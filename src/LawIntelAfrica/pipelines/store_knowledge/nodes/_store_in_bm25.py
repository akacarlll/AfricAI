
import os
import pickle
from typing import Dict
import pandas as pd
from pathlib import Path
from langchain_community.retrievers import BM25Retriever
from langchain.schema import Document
from LawIntelAfrica.utils.data_transformation._df_to_documents import df_to_documents
import logging

logger = logging.getLogger(__name__)    

def create_bm25_stores(
    dataframes_dict: Dict[str, pd.DataFrame],
    split_params: dict, 
    store_type: str = "bm25_stores",
    chunk_text_column: str = "page_content"
) -> None:
    """
    Create BM25 stores from a dictionary of dataframes using LangChain documents.
    
    Args:
        dataframes_dict: Dict with category names as keys and dataframes as values
        output_dir: Directory to save the BM25 store files
        chunk_text_column: Name of the column containing text to embed
    """
    
    base_path = Path(split_params["path"])
    output_dir = base_path / store_type
    os.makedirs(output_dir, exist_ok=True)
    
    for category, df in dataframes_dict.items():

        category_processed_msg = f"Processing category: {category}"
        logging.info(category_processed_msg)

        documents = df_to_documents(df, chunk_text_column, category)
        
        bm25_retriever = BM25Retriever.from_documents(documents)
        category_dir = os.path.join(output_dir, category)
        os.makedirs(category_dir, exist_ok=True)

        store_path = os.path.join(category_dir, f"bm25_index.pkl")
        with open(store_path, 'wb') as f:
            pickle.dump(bm25_retriever, f)
        
        success_msg = f"Successfully created BM25 store created for category: {category}"
        len_doc_msg = f"   - Documents: {len(documents)}"
        logging.info(success_msg)
        logging.info(len_doc_msg)

    vector_stores_msg = f"BM25 stores created"
    logging.info(vector_stores_msg)
import os
import pandas as pd
from langchain.docstore.document import Document
from langchain_community.vectorstores import FAISS
from langchain_huggingface import HuggingFaceEmbeddings
from typing import Dict, List
from LawIntelAfrica.utils.data_transformation._df_to_documents import df_to_documents
import logging
from pathlib import Path

logger = logging.getLogger(__name__)


def create_faiss_vector_stores(
    dataframes_dict: Dict[str, pd.DataFrame],
    split_params: dict,
    store_type: str = "faiss_stores",
    embedding_model: str = "all-MiniLM-L6-v2",
    chunk_text_column: str = "page_content",
) -> None:
    """
    Create FAISS vector stores from a dictionary of dataframes using LangChain documents.

    Args:
        dataframes_dict: Dict with category names as keys and dataframes as values
        output_dir: Directory to save the vector store files
        embedding_model: Name of the sentence transformer model to use
        chunk_text_column: Name of the column containing text to embed
    """
    base_path = Path(split_params["path"])
    output_dir = base_path / store_type
    os.makedirs(output_dir, exist_ok=True)

    loading_model_msg = f"Loading embedding model: {embedding_model}"
    logger.info(loading_model_msg)

    embeddings = HuggingFaceEmbeddings(model_name=embedding_model)

    for category, df in dataframes_dict.items():

        category_processed_msg = f"Processing category: {category}"
        logger.info(category_processed_msg)

        documents = df_to_documents(df, chunk_text_column, category)
        vector_store = FAISS.from_documents(documents, embeddings)
        store_path = os.path.join(output_dir, category)
        vector_store.save_local(store_path)

        success_msg = f"Vector store created for category: {category}"
        len_doc_msg = f"   - Documents: {len(documents)}"
        logger.info(success_msg)
        logger.info(len_doc_msg)

    vector_stores_msg = f"Faiss Vector stores created for categories"
    logger.info(vector_stores_msg)

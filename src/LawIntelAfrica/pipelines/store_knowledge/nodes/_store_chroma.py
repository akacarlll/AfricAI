import os
import pandas as pd
from pathlib import Path
from langchain.docstore.document import Document
from langchain_community.vectorstores import Chroma
from langchain_community.embeddings import HuggingFaceEmbeddings
from typing import Dict
from LawIntelAfrica.utils.data_transformation._df_to_documents import df_to_documents
import logging 

logger = logging.getLogger(__name__)

def create_chroma_vector_stores(
    dataframes_dict: Dict[str, pd.DataFrame],
    split_params: dict,
    store_type: str = "chroma_stores",
    embedding_model: str = "all-MiniLM-L6-v2",
    chunk_text_column: str = "page_content"
)-> None:
    """
    Create Chroma vector stores from a dictionary of dataframes using LangChain documents.
    
    Args:
        dataframes_dict: Dict with category names as keys and dataframes as values
        split_params (dict): A dictionary containing split parameters.
        output_dir: Directory to save the vector store files
        embedding_model: Name of the sentence transformer model to use
        chunk_text_column: Name of the column containing text to embed
    """
    base_path = Path(split_params["path"])
    output_dir = base_path / store_type
    os.makedirs(output_dir, exist_ok=True)

    loading_model_msg = f"Loading embedding model: {embedding_model}"
    logging.info(loading_model_msg)

    embeddings = HuggingFaceEmbeddings(model_name=embedding_model)

    for category, df in dataframes_dict.items():

        category_processed_msg = f"Processing category: {category}"
        logging.info(category_processed_msg)

        documents = df_to_documents(df, chunk_text_column, category)

        persist_directory = os.path.join(output_dir, category)
        vector_store = Chroma.from_documents(
            documents=documents,
            embedding=embeddings,
            collection_name=f"{category}_collection",
            persist_directory=persist_directory
        )

        vector_store.persist()

        success_msg = f"Vector store created for category: {category} at {persist_directory}"
        len_doc_msg = f"   - Documents: {len(documents)}"
        logging.info(success_msg)
        logging.info(len_doc_msg)

    vector_stores_msg = f"Chroma Vector stores created"
    logging.info(vector_stores_msg)

import os
import pandas as pd
from langchain.docstore.document import Document
from langchain_community.vectorstores import FAISS
from langchain_community.embeddings import HuggingFaceEmbeddings
from typing import Dict, List

def create_faiss_vector_stores(
    dataframes_dict: Dict[str, pd.DataFrame],
    output_dir: str = "./vector_stores/faiss_stores",
    embedding_model: str = "all-MiniLM-L6-v2",
    chunk_text_column: str = "chunk_text"
) -> None:
    """
    Create FAISS vector stores from a dictionary of dataframes using LangChain documents.
    
    Args:
        dataframes_dict: Dict with category names as keys and dataframes as values
        output_dir: Directory to save the vector store files
        embedding_model: Name of the sentence transformer model to use
        chunk_text_column: Name of the column containing text to embed
    """
    
    os.makedirs(output_dir, exist_ok=True)
    print(f"Loading embedding model: {embedding_model}")
    embeddings = HuggingFaceEmbeddings(model_name=embedding_model)
    vector_stores = {}
    
    for category, df in dataframes_dict.items():
        print(f"Processing category: {category}")
        if chunk_text_column not in df.columns:
            print(f"Warning: '{chunk_text_column}' column not found in {category} dataframe. Skipping.")
            continue
        documents = df_to_documents(df, chunk_text_column, category)
        print(f"Creating FAISS index for {len(documents)} documents in {category}")
        vector_store = FAISS.from_documents(documents, embeddings)
        store_path = os.path.join(output_dir, category)
        vector_store.save_local(store_path)
        vector_stores[category] = vector_store
        
        print(f"✅ Successfully created FAISS vector store for {category}")
        print(f"   - Store path: {store_path}")
        print(f"   - Documents: {len(documents)}")
        print()
    
    print("🎉 All FAISS vector stores created successfully!")

def df_to_documents(df: pd.DataFrame, chunk_text_column: str, category: str) -> List[Document]:
    """
    Convert a dataframe to LangChain documents.
    
    Args:
        df: DataFrame to convert
        chunk_text_column: Name of the column containing text content
        category: Category name to add to metadata
    
    Returns:
        List of LangChain Document objects
    """
    documents = []
    
    for idx, row in df.iterrows():
        page_content = str(row[chunk_text_column])
        metadata = row.drop(chunk_text_column).to_dict()
        metadata["category"] = category
        metadata = {k: str(v) if not isinstance(v, (str, int, float, bool, type(None))) else v 
                   for k, v in metadata.items()}
        doc = Document(
            page_content=page_content,
            metadata=metadata
        )
        documents.append(doc)
    
    return documents

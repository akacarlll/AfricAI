"""Transfrom a DataFrame to a List of Langchain Documents."""

from langchain.docstore.document import Document
import pandas as pd
import uuid
from typing import List


def df_to_documents(
    df: pd.DataFrame, chunk_text_column: str, category: str
) -> List[Document]:
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
        metadata["doc_id"] = str(uuid.uuid4())

        doc = Document(page_content=page_content, metadata=metadata)
        documents.append(doc)

    return documents

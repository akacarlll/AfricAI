import pandas as pd
from typing import List, Dict, Tuple, Any, Optional
from langchain.text_splitter import RecursiveCharacterTextSplitter


def chunk_legal_documents(
    df: pd.DataFrame, chunk_size: int = 1000, chunk_overlap: int = 200
) -> pd.DataFrame:
    """
    Chunk legal documents from a dataframe into smaller pieces for RAG while respecting document boundaries.
    Uses RecursiveTextSplitter to intelligently split at paragraph and sentence boundaries.

    Parameters:
    -----------
    df : pd.DataFrame
        A DataFrame containing legal documents with at least the following columns:
        - text: The text content of the page
        - page_label: The label/number of the page
        - page_title: The title of the document this page belongs to
        - metadata: Any additional metadata for the document (optional)

    chunk_size : int, optional (default=1000)
        The maximum size of each chunk in characters

    chunk_overlap : int, optional (default=200)
        The amount of overlap between adjacent chunks in characters

    Returns:
    --------
    pd.DataFrame
        A DataFrame with chunked documents including:
        - chunk_id: Unique identifier for each chunk
        - chunk_text: The text content of the chunk
        - document_id: The original document identifier
        - page_labels: The page labels included in this chunk
        - page_title: The title of the document
        - metadata: Original metadata
        - start_char_idx: Start character index in the original document
        - end_char_idx: End character index in the original document
    """
    # Initialize the text splitter with appropriate separators
    # It will try to split on double newlines first, then single newlines, then sentences, etc.
    text_splitter = RecursiveCharacterTextSplitter(
        separators=["\n\n", "\n", ". ", " ", ""],
        chunk_size=chunk_size,
        chunk_overlap=chunk_overlap,
        length_function=len,
    )

    # Group the dataframe by page_title to process each document separately
    grouped = df.groupby("page_title")

    all_chunks = []

    for doc_title, doc_group in grouped:
        # Sort the pages by page_label to ensure correct order
        try:
            doc_group = doc_group.sort_values(
                by="page_label", key=lambda x: x.astype(int)
            )
        except:
            # If page_label is not numeric, sort as strings
            doc_group = doc_group.sort_values(by="page_label")

        # Track page information for mapping chunks back to pages
        full_text = ""
        page_boundaries = {}

        for _, row in doc_group.iterrows():
            start_idx = len(full_text)
            full_text += row["text"] + " "
            end_idx = len(full_text)
            page_boundaries[row["page_label"]] = (start_idx, end_idx)

        if len(full_text) < 1000:
            print(f"Dropping short document - Title: {doc_title}")
            continue  # Skip this document
        # Get metadata if available
        metadata = (
            doc_group["metadata"].iloc[0] if "metadata" in doc_group.columns else {}
        )

        # Use the RecursiveTextSplitter to split the document
        chunks = text_splitter.create_documents(
            [full_text], metadatas=[{"document_id": doc_title}]
        )

        # Process each chunk to add page information
        for i, chunk in enumerate(chunks):
            chunk_start = full_text.find(chunk.page_content)
            chunk_end = chunk_start + len(chunk.page_content)

            # Find which pages this chunk spans
            chunk_pages = []
            for page_label, (page_start, page_end) in page_boundaries.items():
                # If there's any overlap between the chunk and this page
                if not (chunk_end <= page_start or chunk_start >= page_end):
                    chunk_pages.append(page_label)

            # Create chunk entry
            all_chunks.append(
                {
                    "chunk_id": f"{doc_title}_{i}",
                    "chunk_text": chunk.page_content,
                    "document_id": doc_title,
                    "page_labels": chunk_pages,
                    "page_title": doc_title,
                    "metadata": metadata,
                    "start_char_idx": chunk_start,
                    "end_char_idx": chunk_end,
                }
            )

    return pd.DataFrame(all_chunks)


def chunk_legal_corpus(
    df: pd.DataFrame, chunk_size: int = 1000, chunk_overlap: int = 250
) -> pd.DataFrame:
    """
    Process a corpus of legal documents and chunk them for RAG using RecursiveTextSplitter.

    Parameters:
    -----------
    df : pd.DataFrame
        The input DataFrame containing legal documents

    output_path : str, optional
        If provided, save the chunked documents to this path

    chunk_size : int, optional (default=1000)
        The maximum size of each chunk in characters

    chunk_overlap : int, optional (default=200)
        The amount of overlap between adjacent chunks in characters

    Returns:
    --------
    pd.DataFrame
        A DataFrame with chunked documents
    """
    required_columns = ["text", "page_label", "page_title"]
    for col in required_columns:
        if col not in df.columns:
            raise ValueError(f"Input DataFrame missing required column: {col}")

    if "metadata" not in df.columns:
        df["metadata"] = None

    chunked_df = chunk_legal_documents(df, chunk_size, chunk_overlap)

    return chunked_df

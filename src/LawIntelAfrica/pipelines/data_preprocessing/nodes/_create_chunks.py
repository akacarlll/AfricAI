import pandas as pd
from langchain.text_splitter import RecursiveCharacterTextSplitter
import logging

logger = logging.getLogger(__name__)


def chunk_legal_documents(
    df: pd.DataFrame, chunk_size: int = 1000, chunk_overlap: int = 200
) -> pd.DataFrame:
    """
    Chunk legal documents from a dataframe into smaller pieces for RAG while respecting document boundaries.
    Uses RecursiveTextSplitter to intelligently split at paragraph and sentence boundaries.

    Parameters:
    -----------
    df : pd.DataFrame
        A DataFrame containing legal documents with the following columns:
        - page_content: The text content of the page
        - page_label: The label/number of the page
        - page_title: The title of the document this page belongs to
        - folder, source, text_length, URL, category, year, year_maybe, country,
          language, Claimant, Chamber, Against, Appeal, Judgment, Case,
          Defendant, Court, Section, file_type: Additional metadata columns

    chunk_size : int, optional (default=1000)
        The maximum size of each chunk in characters

    chunk_overlap : int, optional (default=200)
        The amount of overlap between adjacent chunks in characters

    Returns:
    --------
    pd.DataFrame
        A DataFrame with chunked documents including:
        - chunk_id: Unique identifier for each chunk
        - page_content: The text content of the chunk
        - document_id: The original document identifier (page_title)
        - page_labels: The page labels included in this chunk
        - page_title: The title of the document
        - start_char_idx: Start character index in the original document
        - end_char_idx: End character index in the original document
        - All original metadata columns preserved
    """
    text_splitter = RecursiveCharacterTextSplitter(
        separators=["\n\n", "\n", ". ", " ", ""],
        chunk_size=chunk_size,
        chunk_overlap=chunk_overlap,
        length_function=len,
    )

    grouped = df.groupby("page_title")
    all_chunks = []

    for doc_title, doc_group in grouped:
        try:
            doc_group = doc_group.sort_values(
                by="page_label", key=lambda x: x.astype(int)
            )
        except:
            doc_group = doc_group.sort_values(by="page_label")

        full_text = ""
        page_boundaries = {}

        for _, row in doc_group.iterrows():
            start_idx = len(full_text)
            full_text += row["page_content"] + " "
            end_idx = len(full_text)
            page_boundaries[row["page_label"]] = (start_idx, end_idx)

        if len(full_text) < 200:
            dropped_docs_msg = f"Dropping short document - Title: {doc_title}. Length: {len(full_text)}"
            logger.info(dropped_docs_msg)
            continue

        first_row = doc_group.iloc[0]
        document_metadata = {
            col: first_row[col]
            for col in df.columns
            if col not in ["page_content", "page_label", "text_length"]
        }

        chunks = text_splitter.create_documents(
            [full_text], metadatas=[{"document_id": doc_title}]
        )

        for i, chunk in enumerate(chunks):
            chunk_start = full_text.find(chunk.page_content)
            chunk_end = chunk_start + len(chunk.page_content)

            chunk_pages = []
            for page_label, (page_start, page_end) in page_boundaries.items():
                if not (chunk_end <= page_start or chunk_start >= page_end):
                    chunk_pages.append(page_label)

            chunk_record = {
                "chunk_id": f"{doc_title}_{i}",
                "page_content": chunk.page_content,
                "document_id": doc_title,
                "page_labels": chunk_pages,
                "start_char_idx": chunk_start,
                "end_char_idx": chunk_end,
                "chunk_length": len(chunk.page_content),
                "num_pages_spanned": len(chunk_pages),
            }

            chunk_record.update(document_metadata)

            all_chunks.append(chunk_record)

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

    if "metadata" not in df.columns:
        df["metadata"] = None

    return chunk_legal_documents(df, chunk_size, chunk_overlap)

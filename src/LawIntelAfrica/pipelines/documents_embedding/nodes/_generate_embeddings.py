from sentence_transformers import SentenceTransformer
import numpy as np
import pandas as pd
from typing import List, Optional


def generate_embeddings(
    df: pd.DataFrame, model_name: str, batch_size: int = 8, show_progress: bool = True
) -> pd.DataFrame:
    """
    Generates embeddings in batches and adds them to the DataFrame.

    Args:
        df: DataFrame with a "chunk_text" column.
        model_name: Name of the SentenceTransformer model.
        batch_size: Number of texts processed per batch.
        show_progress: Whether to show a progress bar.

    Returns:
        DataFrame with an added "embedding" column.
    """
    model = SentenceTransformer(model_name)
    texts = df["chunk_text"].tolist()

    # Batch processing
    embeddings = model.encode(
        texts,
        batch_size=batch_size,
        convert_to_numpy=True,
        show_progress_bar=show_progress,
    )

    df["embedding"] = embeddings.tolist()
    return df

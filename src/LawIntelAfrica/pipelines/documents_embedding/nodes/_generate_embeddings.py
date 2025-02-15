from sentence_transformers import SentenceTransformer
import numpy as np
import pandas as pd

def generate_embeddings(df: pd.DataFrame, model_name: str) -> np.ndarray:
    """
    Convertit une liste de textes en embeddings en utilisant un modèle de Sentence Transformers.

    Args:
        texts (pd.Series): Série Pandas contenant les textes.
        model_name (str): Nom du modèle Sentence Transformers.

    Returns:
        np.ndarray: Matrice d'embeddings.
    """
    model = SentenceTransformer(model_name)
    embeddings = model.encode(df["text"].tolist(), convert_to_numpy=True)
    df["embedding"] = list(embeddings) 
    
    return df, embeddings

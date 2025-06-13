import os
import pandas as pd
from qdrant_client import QdrantClient
from qdrant_client.http.exceptions import QdrantException
from qdrant_client.models import Distance, VectorParams, PointStruct
from sentence_transformers import SentenceTransformer
from typing import Dict, Optional
import uuid

def create_qdrant_vector_stores(
    dataframes_dict: Dict[str, pd.DataFrame],
    output_dir: str = "./vector_stores/qdrant",
    embedding_model: str = "all-MiniLM-L6-v2",
    vector_size: int = 384,
    distance_metric: Distance = Distance.COSINE,
    chunk_text_column: str = "chunk_text"
)-> None:
    """
    Create Qdrant vector stores from a dictionary of dataframes.
    
    Args:
        dataframes_dict: Dict with category names as keys and dataframes as values
        output_dir: Directory to save the vector store files
        embedding_model: Name of the sentence transformer model to use
        vector_size: Size of the embedding vectors (384 for all-MiniLM-L6-v2)
        distance_metric: Distance metric for similarity search
        chunk_text_column: Name of the column containing text to embed
    """
    os.makedirs(output_dir, exist_ok=True)
    
    print(f"Loading embedding model: {embedding_model}")
    model = SentenceTransformer(embedding_model)
    
    # Dictionary to store client instances
    clients = {}
    
    for category, df in dataframes_dict.items():
        print(f"Processing category: {category}")
        if chunk_text_column not in df.columns:
            print(f"Warning: '{chunk_text_column}' column not found in {category} dataframe. Skipping.")
            continue
        db_path = os.path.join(output_dir, f"{category}.db")
        client = QdrantClient(path=db_path)
        collection_name = f"{category}_collection"
        try:
            client.delete_collection(collection_name)
        except QdrantClientException:
            pass 
        client.create_collection(
            collection_name=collection_name,
            vectors_config=VectorParams(
                size=vector_size,
                distance=distance_metric
            )
        )
        
        texts = df[chunk_text_column].tolist()
        df = df.drop(columns=[chunk_text_column])
        print(f"Generating embeddings for {len(texts)} chunks in {category}")
        embeddings = model.encode(texts, show_progress_bar=True)
        
        points = []
        for idx, (text, embedding) in enumerate(zip(texts, embeddings)):
            metadata = df.iloc[idx].to_dict()
            point = PointStruct(
                id=str(uuid.uuid4()),
                vector=embedding.tolist(),
                payload={
                    "text": text,
                    "metadata": metadata,
                    "category": category
                }
            )
            points.append(point)
        
        print(f"Inserting {len(points)} points into {category} collection")
        client.upsert(
            collection_name=collection_name,
            points=points
        )
        
        clients[category] = {
            "client": client,
            "collection_name": collection_name,
            "db_path": db_path
        }
        
        print(f"✅ Successfully created vector store for {category}")
        print(f"   - Database path: {db_path}")
        print(f"   - Collection: {collection_name}")
        print(f"   - Points inserted: {len(points)}")
    
    print("🎉 All vector stores created successfully!")


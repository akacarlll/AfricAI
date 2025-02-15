"""
This is a boilerplate pipeline 'documents_embedding'
generated using Kedro 0.19.10
"""

from kedro.pipeline import Pipeline, pipeline,node
from .nodes import (
    generate_embeddings,
    assign_unique_ids,
    store_in_chroma,
)


def create_pipeline(**kwargs) -> Pipeline:
    return pipeline([
        node(
            func=assign_unique_ids,
            inputs="chunked_docs",
            outputs="docs_unique_id",
            name="assign_unique_ids",
        ),
        node(
            func=generate_embeddings,
            inputs=["docs_unique_id", "params:model_name"],
            outputs=["df_embedding", "stored_embeddings"],
            name="generate_embeddings",
        ),
        node(
            func=store_in_chroma,
            inputs=["df_embedding", "params:chroma"],
            outputs=None,
            name="store_in_chroma",
        )               
])

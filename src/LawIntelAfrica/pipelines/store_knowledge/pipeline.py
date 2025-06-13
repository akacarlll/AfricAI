"""
This is a boilerplate pipeline 'store_knowledge'
generated using Kedro 0.19.10
"""

from kedro.pipeline import Pipeline, pipeline, node
from .nodes import (
    create_chroma_vector_stores,
    create_faiss_vector_stores,
    create_qdrant_vector_stores,
    split_data,
)


def _modular_pipeline(**kwargs) -> Pipeline:
    return pipeline(
        [
            node(
                func=split_data,
                inputs=["chunked_docs", "params:split_params"],
                outputs="split_dfs",
                name="splitting_data",
            ),
            node(
                func=create_chroma_vector_stores,
                inputs=["split_dfs"],
                outputs=None,
                name="store_in_chroma",
            ),
            node(
                func=create_qdrant_vector_stores,
                inputs=["split_dfs"],
                outputs=None,
                name="store_in_qdrant"
            ),
            node(
                func=create_faiss_vector_stores,
                inputs=["split_dfs"],
                outputs=None,
                name="store_in_faiss"
            ),
        ]
    )


def create_pipeline(**kwargs) -> Pipeline:
    pipeline1 = pipeline(
        pipe=_modular_pipeline(),
        namespace="split1",
        inputs={"chunked_docs": "chunked_docs"},
        parameters={
            "params:split_params": "params:split_params_1",
        },
    )
    pipeline2 = pipeline(
        pipe=_modular_pipeline(),
        namespace="split2",
        inputs={"chunked_docs": "chunked_docs"},
        parameters={
            "params:split_params": "params:split_params_2",
        },
    )
    return pipeline1 

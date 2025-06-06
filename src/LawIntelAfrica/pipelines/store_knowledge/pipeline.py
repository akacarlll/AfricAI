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
                inputs=["df_embedding", "params:split_params"],
                outputs="split_dfs",
                name="splitting_data",
            ),
            node(
                func=create_chroma_vector_stores,
                inputs=["split_dfs", "params:chroma_params"],
                outputs=None,
                name="store_in_chroma",
            ),
            node(
                func=create_qdrant_vector_stores,
                inputs=["splits_dfs", "params:qdrant_params"],
                outputs=None,
                name="store_in_qdrant"
            ),
            node(
                func=create_faiss_vector_stores,
                inputs=["splits_dfs", "params:faiss_params"],
                outputs=None,
                name="store_in_faiss"
            ),
        ]
    )


def create_pipeline(**kwargs) -> Pipeline:
    pipeline1 = pipeline(
        pipe=_modular_pipeline(),
        namespace="split1",
        inputs={"df_embedding": "df_embedding"},
        parameters={
            "params:split_params": "params:split_params_1",
            "params:chroma_params": "params:chroma_params_1",
        },
    )
    pipeline2 = pipeline(
        pipe=_modular_pipeline(),
        namespace="split2",
        inputs={"df_embedding": "df_embedding"},
        parameters={
            "params:split_params": "params:split_params_2",
            "params:chroma_params": "params:chroma_params_2",
        },
    )
    return pipeline1 + pipeline2

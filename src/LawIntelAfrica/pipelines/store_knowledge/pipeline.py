"""This module contains the pipelines to store the vector stores"""

from kedro.pipeline import Pipeline, pipeline, node
from .nodes import (
    create_chroma_vector_stores,
    create_faiss_vector_stores,
    create_qdrant_vector_stores,
    create_bm25_stores,
    split_data,
)


def create_modular_pipeline() -> Pipeline:
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
                inputs=["split_dfs", "params:split_params"],
                outputs=None,
                name="store_in_chroma",
            ),
            # node(
            #     func=create_qdrant_vector_stores,  # TODO: Fix the function, it does nothing for now.
            #     inputs=["split_dfs", "params:split_params"],
            #     outputs=None,
            #     name="store_in_qdrant",
            # ),
            node(
                func=create_faiss_vector_stores,
                inputs=["split_dfs", "params:split_params"],
                outputs=None,
                name="store_in_faiss",
            ),
            node(
                func=create_bm25_stores,
                inputs=["split_dfs", "params:split_params"],
                outputs=None,
                name="store_in_bm25",
            ),
        ]
    )


def create_pipeline() -> Pipeline:
    pipeline1 = pipeline(
        pipe=create_modular_pipeline(),
        namespace="save_per_category",
        inputs={"chunked_docs": "chunked_docs"},
        parameters={
            "params:split_params": "params:split_params_1",
        },
    )
    pipeline2 = pipeline(
        pipe=create_modular_pipeline(),
        namespace="save_no_category",
        inputs={"chunked_docs": "chunked_docs"},
        parameters={
            "params:split_params": "params:split_params_2",
        },
    )
    return pipeline1

"""This module contains the pipelines to store the vector stores"""

from kedro.pipeline import Pipeline, pipeline, node
from .nodes import (
    create_chroma_vector_stores,
    create_faiss_vector_stores,
    create_qdrant_vector_stores,
    create_bm25_stores,
    filter_on_year,
    split_data,
)


def create_modular_pipeline() -> Pipeline:
    return pipeline(
        [
            node(
                func=filter_on_year,
                inputs=["chunked_docs", "params:split_params"],
                outputs="filtered_by_year_docs",
                name="filter_by_year_node",
            ),
            node(
                func=split_data,
                inputs=["filtered_by_year_docs"],
                outputs="split_dfs",
                name="split_data_node",
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
        create_modular_pipeline(),
        namespace="save_per_category",
        inputs={"chunked_docs": "chunked_docs"},
        parameters={
            "params:split_params": "params:split_params_1",
        },
    )
    pipeline2 = pipeline(
        create_modular_pipeline(),
        namespace="save_no_category",
        inputs={"chunked_docs": "chunked_docs"},
        parameters={
            "params:split_params": "params:split_params_2",
        },
    )
    return pipeline1 + pipeline2

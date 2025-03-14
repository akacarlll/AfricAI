"""
This is a boilerplate pipeline 'store_knowledge'
generated using Kedro 0.19.10
"""

from kedro.pipeline import Pipeline, pipeline, node
from .nodes import (
    store_in_chroma,
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
                func=store_in_chroma,
                inputs=["split_df", "params:chroma_params"],
                outputs=None,
                name="store_in_chroma",
            ),
        ]
    )


def create_pipeline(**kwargs) -> Pipeline:
    pipeline1 = pipeline(
        pipe=_modular_pipeline(),
        namespace="split1",
        inputs={"df_embedding": "df_embedding"},
        parameters={"params:split_params": "params:split_params_1"},
    )
    pipeline2 = pipeline(
        pipe=_modular_pipeline(),
        namespace="split2",
        inputs={"df_embedding": "df_embedding"},
        parameters={"params:split_params": "params:split_params_2"},
    )
    return pipeline1 + pipeline2

from kedro.pipeline import Pipeline, pipeline, node
from .nodes import (
    generate_embeddings,
    assign_unique_ids,
)


def create_pipeline(**kwargs) -> Pipeline:
    return pipeline(
        [
            node(
                func=generate_embeddings,
                inputs=["chunked_docs", "params:model_name"],
                outputs="df_embedding",
                name="generate_embeddings",
            ),
        ]
    )

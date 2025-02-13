"""
This is a boilerplate pipeline 'data_preprocessing'
generated using Kedro 0.19.10
"""
from .nodes import (
    clean_text,
    clean_noise,
    replace_words,
)

from kedro.pipeline import Pipeline, pipeline, node


def create_pipeline(**kwargs) -> Pipeline:
    return pipeline([
        node(
                func=clean_noise,
                inputs="cleaned_legal_documents",
                outputs="noiseless_doc",
                name="remove_noise_node",
        ),
        node(
            func=clean_text,
            inputs="noiseless_doc",
            outputs="cleaned_text",
            name="clean_text_node",
        ),
        node(
            func=replace_words,
            inputs="cleaned_text",
            outputs="preprocessed_docs",
            name="replace_words_node",
        ),
    ])

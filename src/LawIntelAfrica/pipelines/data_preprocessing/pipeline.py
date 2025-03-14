"""
This is a boilerplate pipeline 'data_preprocessing'
generated using Kedro 0.19.10
"""

from .nodes import (
    clean_text,
    replace_words,
    remove_redundance,
    chunk_legal_corpus,
)

from kedro.pipeline import Pipeline, pipeline, node


def create_pipeline(**kwargs) -> Pipeline:
    return pipeline(
        [
            node(
                func=clean_text,
                inputs="cleaned_legal_documents",
                outputs="cleaned_text",
                name="clean_text_node",
            ),
            node(
                func=replace_words,
                inputs="cleaned_text",
                outputs="replaced_text",
                name="replace_words_node",
            ),
            node(
                func=remove_redundance,
                inputs="replaced_text",
                outputs="preprocessed_docs",
                name="remove_redundance_node",
            ),
            node(
                func=chunk_legal_corpus,
                inputs=["preprocessed_docs", "params:chunk_size"],
                outputs="chunked_docs",
                name="chunk_text_node",
            ),
        ]
    )

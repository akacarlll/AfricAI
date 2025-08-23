from kedro.pipeline import Pipeline, node, pipeline

from .nodes import (
    load_documents,
    extract_metadata,
    remove_characters,
    merge_pdfs_texts_dfs,
)


def create_pipeline(**kwargs) -> Pipeline:
    """
    Create a Kedro pipeline for processing legal documents.

    Args:
        **kwargs (Dict[str, Any]): Additional keyword arguments for pipeline configuration.

    Returns:
        Pipeline: A Kedro pipeline with nodes for loading, merging, extracting metadata, and cleaning legal documents.
    """
    return pipeline(
        [
            node(
                func=load_documents,
                inputs="params:data_path",
                outputs="df_legal_documents",
                name="load_legal_documents",
            ),
            node(
                func=merge_pdfs_texts_dfs,
                inputs=["df_legal_documents", "params:folder_params"],
                outputs="merged_data",
                name="merge_pdfs_and_texts",
            ),
            node(
                func=extract_metadata,
                inputs="merged_data",
                outputs="metadata_legal_documents",
                name="extract_legal_documents",
            ),
            node(
                func=remove_characters,
                inputs="metadata_legal_documents",
                outputs="cleaned_legal_documents",
                name="clean_legal_documents",
            ),
        ]
    )

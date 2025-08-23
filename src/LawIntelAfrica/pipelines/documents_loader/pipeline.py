from kedro.pipeline import Pipeline, node, pipeline

from .nodes import (
    load_documents,
    extract_metadata,
    remove_characters,
    merge_pdfs_texts_dfs,
)


def create_modular_pipeline(country: str) -> Pipeline:
    """Create a Kedro modular pipeline for processing legal documents.

    Args:
        country (str): country (str): The country for which the pipeline is created.

    Returns:
        Pipeline: A Kedro pipeline with nodes for loading, merging, extracting metadata, and cleaning legal documents.
    """
    return pipeline(
        [
            node(
                func=load_documents,
                inputs=["params:data_path", country],
                outputs="df_legal_documents",
                name="load_legal_documents",
            ),
            node(
                func=merge_pdfs_texts_dfs,
                inputs=["df_legal_documents", "params:folder_params", country],
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


def create_pipeline() -> dict[str, Pipeline]:
    """
    Create a pipeline with several modular pipelines.

    Returns:
        dict[str, Pipeline]: A dictionary mapping country names to their respective pipelines.
    """
    countries_to_run = ["ben", "cmr"]
    pipelines = {}
    for country in countries_to_run:
        pipelines[f"{country}_document_loader"] = create_modular_pipeline(country)
    return pipelines

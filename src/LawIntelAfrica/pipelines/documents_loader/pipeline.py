from kedro.pipeline import Pipeline, node, pipeline

from .nodes import (
    load_documents,
    extract_metadata,
    remove_characters,
    merge_pdfs_texts_dfs,
    verify_columns,
)


def create_pipeline(**kwargs) -> Pipeline:
    return pipeline(
        [
            node(
                func=load_documents,
                inputs="params:data_path",
                outputs="df_legal_documents",
                name="load_legal_documents",
            ),
            # TODO : Add a node to parse tables in the pdfs
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
            node(
                func=verify_columns, #TODO remove this node and create a Hook to verify the columns throughout the entire project.
                inputs=["cleaned_legal_documents", "params:expected_columns"],
                outputs= None,
                name="validate_legal_documents",
            ),
        ]
    )

from kedro.pipeline import Pipeline, node, pipeline

from .nodes import (
    load_documents, 
    extract_metadata, 
    remove_characters,
    merge_pdfs_texts_dfs,
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
                func=extract_metadata,
                inputs="df_legal_documents",  
                outputs="metadata_legal_documents",
                name="extract_legal_documents",
            ),
            node(
                func=merge_pdfs_texts_dfs,
                inputs=["metadata_legal_documents", "params:folder_params"],
                outputs="merged_data",
                name="merge_pdfs_and_texts"
            ),
            node(
                func=remove_characters,
                inputs="merged_data",
                outputs="cleaned_legal_documents",
                name="clean_legal_documents",
                
            ),

        ]
    )

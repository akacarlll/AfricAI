from kedro.pipeline import Pipeline, node, pipeline

from .nodes import (load_documents, 
    extract_metadata, 
    transform_list_to_df,
    remove_characters
    )


def create_pipeline(**kwargs) -> Pipeline:
    return pipeline(
        [
            node(
                func=load_documents,
                inputs="params:data_path",
                outputs="legal_documents",
                name="load_legal_documents",
            ),
            node(
                func=transform_list_to_df,
                inputs="legal_documents",
                outputs="df_legal_documents",
                name="transform_legal_documents",
            ),
            node(
                func=extract_metadata,
                inputs="df_legal_documents",  
                outputs="metadata_legal_documents",
                name="extract_legal_documents",
            ),
            node(
                func=remove_characters,
                inputs="metadata_legal_documents",
                outputs="cleaned_legal_documents",
                name="clean_legal_documents",
                
            )

        ]
    )

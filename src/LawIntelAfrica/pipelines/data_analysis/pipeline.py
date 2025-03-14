from kedro.pipeline import Pipeline, pipeline, node
from .nodes import (
    analyze_data_preprocessing,
    analyze_documents_embedding,
    analyze_documents_loader,
    analyze_store_knowledge,
)


def create_pipeline(**kwargs) -> Pipeline:
    return pipeline(
        [
            node(
                func=analyze_documents_loader,
                inputs="cleaned_legal_documents",
                outputs="documents_loader_analysis",
                name="analyze_documents_loader",
            ),
            node(
                func=analyze_data_preprocessing,
                inputs="chunked_docs",
                outputs="data_preprocessing_analysis",
                name="analyze_data_preprocessing",
            ),
            node(
                func=analyze_documents_embedding,
                inputs="df_embedding",
                outputs="documents_embedding_analysis",
                name="analyze_documents_embedding",
            ),
            node(
                func=analyze_store_knowledge,
                inputs=["split1.split_dfs", "split2.split_dfs"],
                outputs="store_knowledge_analysis",
                name="analyze_store_knowledge",
            ),
            node(
                func=merge_results,
                inputs=[
                    "documents_loader_analysis",
                    "data_preprocessing_analysis",
                    "documents_embedding_analysis",
                    "store_knowledge_analysis",
                ],
                outputs="data_analysis_results",
                name="merge_results",
            ),
        ]
    )

"""Project pipelines for LawIntelAfrica."""

from typing import Dict
from kedro.pipeline import Pipeline

import LawIntelAfrica.pipelines.documents_loader as dl
import LawIntelAfrica.pipelines.data_preprocessing as dp
import LawIntelAfrica.pipelines.documents_embedding as de
import LawIntelAfrica.pipelines.store_knowledge as sk
from LawIntelAfrica.pipelines import data_analysis as da


def register_pipelines() -> Dict[str, Pipeline]:
    """Register project pipelines.

    Returns:
        Dict[str, Pipeline]: A mapping import pipeline names to ``Pipeline`` objects.
    """
    # Individual pipelines
    doc_loader_pipeline = dl.create_pipeline()
    doc_preprocessing_pipeline = dp.create_pipeline()
    doc_embedding_pipeline = de.create_pipeline()
    store_knowledge_pipeline = sk.create_pipeline()
    doc_analysis_pipeline = da.create_pipeline()

    # Combined pipelines for specific workflows
    data_processing_pipeline = doc_loader_pipeline + doc_preprocessing_pipeline
    full_pipeline = (
        doc_embedding_pipeline + data_processing_pipeline + store_knowledge_pipeline
    )

    return {
        "__default__": full_pipeline,
        # Individual pipeline components
        "documents_loader": doc_loader_pipeline,
        "data_preprocessing": doc_preprocessing_pipeline,
        "documents_embedding": doc_embedding_pipeline,
        "store_knowledge": store_knowledge_pipeline,
        "data_analysis": doc_analysis_pipeline,
        # Composite pipelines
        "data_processing": data_processing_pipeline,
        "full_pipeline": full_pipeline,
    }

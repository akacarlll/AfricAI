"""Project pipelines."""

from kedro.pipeline import Pipeline
from LawIntelAfrica.pipelines.documents_loader import create_pipeline as data_loading_pipeline
from LawIntelAfrica.pipelines.data_preprocessing import create_pipeline as data_preprocessing_pipeline


def register_pipelines():
    return {
        "__default__": data_loading_pipeline(),
        "document_loader": data_loading_pipeline(),
        "document_preprocessing": data_preprocessing_pipeline(),
    }
    
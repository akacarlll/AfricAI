"""Project pipelines."""

from kedro.framework.project import find_pipelines
from kedro.pipeline import Pipeline


# def register_pipelines() -> dict[str, Pipeline]:
#     """Register the project's pipelines.

#     Returns:
#         A mapping from pipeline names to ``Pipeline`` objects.
#     """
#     pipelines = find_pipelines()
#     pipelines["__default__"] = sum(pipelines.values())
#     return pipelines
from LawIntelAfrica.pipelines.documents_loader import create_pipeline as data_processing_pipeline

def register_pipelines():
    return {
        "__default__": data_processing_pipeline(),
        "document_loader": data_processing_pipeline(),
    }
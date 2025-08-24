from kedro.pipeline import Pipeline, pipeline, node
from .nodes import create_countries_legal_documentation_dict, plot_country_docs


def create_pipeline() -> Pipeline:
    return pipeline(
        [
            node(
                func=create_countries_legal_documentation_dict,
                inputs=None,
                outputs="countries_legal_doc_dict",
                name="create_countries_legal_documentation_dict_node",
            ),
            node(
                func=plot_country_docs,
                inputs="countries_legal_doc_dict",
                outputs="legal_docs_world_map",
                name="plot_country_docs_node",
            ),
        ]
    )

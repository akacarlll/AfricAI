from kedro.pipeline import Pipeline, pipeline, node
from .nodes import create_countries_legal_documentation_dict, plot_country_docs, create_year_title_bar_plot


def create_pipeline() -> Pipeline:
    return pipeline(
        [
            node(
                func=create_countries_legal_documentation_dict,
                inputs=None,
                outputs=["countries_legal_doc_dict", "countries_year_doc_dict"],
                name="create_countries_legal_documentation_dict_node",
            ),
            node(
                func=plot_country_docs,
                inputs="countries_legal_doc_dict",
                outputs="legal_docs_world_map",
                name="plot_country_docs_node",
            ),
            node(
                func=create_year_title_bar_plot,
                inputs="countries_year_doc_dict",
                outputs="year_title_bar_plot",# TODO: fix the function output a dict, the plot can't be saved
                name="create_year_title_bar_plot_node",
            )
        ]
    )

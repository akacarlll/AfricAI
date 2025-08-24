from ._join_text_in_single_list import join_text_in_single_list
from ._merges_results import merge_results
from ._countries_legal_doc_description_dict import (
    create_countries_legal_documentation_dict,
)
from ._create_map_plot import plot_country_docs
from ._create_year_plot import create_year_title_bar_plot

__all__ = [
    "join_text_in_single_list",
    "merge_results",
    "create_countries_legal_documentation_dict",
    "plot_country_docs",
    "create_year_title_bar_plot"
]

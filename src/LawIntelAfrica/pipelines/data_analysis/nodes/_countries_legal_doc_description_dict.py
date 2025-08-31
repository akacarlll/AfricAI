import pandas as pd

from collections import defaultdict
from LawIntelAfrica.utils.utils import COUNTRIES_TO_RUN


def create_countries_legal_documentation_dict() -> set[dict]:
    """
    Creates a dictionary summarizing the count of legal document categories for each country.

    Returns:
        dict: Dictionary with country names as keys and category counts as values.
    """
    countries_description_dict = defaultdict(dict)
    title_year_dict = defaultdict(lambda: defaultdict(list))
    for country in COUNTRIES_TO_RUN:
        legal_doc = pd.read_csv(
            f"data/02_intermediate/{country}_loaded_legal_documents.csv"
        )
        aggregated_df = aggregate_dataframe(legal_doc)

        category_counts = aggregated_df["category"].value_counts().to_dict()

        for year, group in aggregated_df.groupby("year"):
            titles = group["page_title"].tolist()
            title_year_dict[country.upper()][year] = titles

        countries_description_dict[country.upper()] = category_counts

    return dict(countries_description_dict), dict(title_year_dict) # type: ignore


def aggregate_dataframe(legal_doc: pd.DataFrame) -> pd.DataFrame:
    """
    Aggregates the legal document DataFrame by 'page_title'.

    Args:
        legal_doc (pd.DataFrame): DataFrame containing legal documents.

    Returns:
        pd.DataFrame: Aggregated DataFrame.
    """
    legal_doc["page_content"] = str(legal_doc["page_content"])
    return (
        legal_doc.groupby("page_title")
        .agg(
            {
                "page_content": lambda x: "\n".join(x),
                **{
                    col: "first"
                    for col in legal_doc.columns
                    if col not in ["page_title", "page_content"]
                },
            }
        )
        .reset_index()
    )

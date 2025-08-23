import pandas as pd
from collections import defaultdict


def join_text_in_single_list(
    cleaned_legal_documents: pd.DataFrame,
) -> dict[str, list[str]]:
    """"""
    text_dict = defaultdict(list)
    for _, row in cleaned_legal_documents.iterrows():
        text = row["page_content"]
        title = row["page_title"]
        text_dict[title].extend(f"\n {text}")

    return text_dict

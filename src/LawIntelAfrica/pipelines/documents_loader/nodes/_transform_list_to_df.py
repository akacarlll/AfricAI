import pandas as pd 


def transform_list_to_df(documents: list) -> pd.DataFrame:
    """Transforms a list of documents into a DataFrame.

    This function takes a list of documents and converts it into a DataFrame
    for further processing.

    Args:
        documents (list): A list of documents.

    Returns:
        pd.DataFrame: A DataFrame containing the documents.
    """
    
    # Appliquer la fonction à tous les documents
    data = [document_to_dict(page) for page in documents]
    df = pd.DataFrame(data)
    return df

def document_to_dict(page):
    """
    Convertit un objet Document en dictionnaire pour le DataFrame.
    """
    doc_dict = {
        "text": page.page_content
    }
    
    # Ajouter toutes les métadonnées disponibles
    for key, value in page.metadata.items():
        doc_dict[key] = value
    
    return doc_dict

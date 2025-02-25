from langchain_community.document_loaders import PyPDFDirectoryLoader
import pandas as pd 
import os


def load_documents(data_path: str) -> pd.DataFrame:
    """
    Loads documents from all subfolders under the specified directory and returns them as a Pandas DataFrame.

    This function iterates over all subfolders in the given data_path, uses PyPDFDirectoryLoader to load documents
    from each subfolder, transform them into datataframes and concatenates them into a single DataFrame.

    Args:
        data_path (str): The path to the directory containing subfolders with documents.

    Returns:
        pd.DataFrame: A DataFrame containing all loaded documents from all subfolders.

    """
    # Liste pour stocker les DataFrames de chaque sous-dossier
    dataframes = []

    # Parcourir tous les sous-dossiers de data_path
    for root, dirs, files in os.walk(data_path):
        # Ignorer le dossier racine (data_path lui-même) si nécessaire
        if root == data_path:
            continue

        # Charger les documents du sous-dossier actuel
        document_loader = PyPDFDirectoryLoader(root)
        documents = document_loader.load()

        # Convertir les documents en DataFrame et l'ajouter à la liste
        if documents:  # Vérifier si des documents ont été chargés
            df = transform_list_to_df(documents)
            dataframes.append(df)
            print(f"Folder converted: {root}")

    # Concaténer tous les DataFrames en un seul
    if dataframes:
        combined_df = pd.concat(dataframes, ignore_index=True)
        return combined_df
    else:
        print("Aucun document trouvé dans les sous-dossiers.")
        return pd.DataFrame()  # Retourne un DataFrame vide si aucun document n'est trouvé

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
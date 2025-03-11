import os
import pandas as pd
from tqdm import tqdm


def merge_pdfs_texts_dfs(df: pd.DataFrame, base_folder: str) -> pd.DataFrame:
    """
    Merges a given DataFrame with text data loaded from multiple subfolders in a base folder.

    This function loads text data from all subfolders within the specified base folder using
    `load_and_concat_dataframes`, then concatenates it with the input DataFrame.

    Args:
        df (pd.DataFrame): The input DataFrame to merge with the text data.

    Returns:
        pd.DataFrame: A single DataFrame resulting from the concatenation of the input DataFrame
                     and the text data loaded from the base folder.

    """
    df2 = load_and_concat_dataframes(base_folder)
    merged_df = pd.concat([df, df2], ignore_index=True)
    return merged_df


def load_and_concat_dataframes(base_folder):
    """
    Loads and concatenates all files of a specified type (default: CSV) from subfolders of a base folder.

    Args:
        base_folder (str): Path to the base folder containing subfolders.
        file_extension (str): File extension to load (default: "csv").

    Returns:
        pd.DataFrame: A single DataFrame containing all concatenated data.

    Raises:
        ValueError: If the file extension is not supported.

    Notes:
        - Supported file extensions: "csv", "xlsx", "xls".
        - If no files are found, an empty DataFrame is returned.
    """
    # Liste pour stocker les DataFrames
    dataframes = []

    # Parcourir tous les sous-dossiers et fichiers
    for root, _, files in os.walk(base_folder):
        for file in tqdm(files):
            # Vérifier si le fichier a l'extension souhaitée
            if file.endswith(f".csv"):
                file_path = os.path.join(root, file)
                df = pd.read_csv(file_path)
                dataframes.append(df)
    if dataframes:
        combined_df = pd.concat(dataframes, ignore_index=True)
        print("Text data entirely merged !")
        return combined_df
    else:
        print("Aucun fichier trouvé.")
        return pd.DataFrame()

def analyze_documents_loader(df):
    # Analysis logic for documents_loader pipeline
    analysis_result = df.describe().to_json()
    with open("documents_loader_analysis.json", "w") as f:
        f.write(analysis_result)
    return analysis_result


import os
from typing import Dict, Set
import pandas as pd


def count_files_in_folder(
    folder_path: str, extensions: Set[str] = {".csv", ".pdf"}
) -> Dict[str, int]:
    """
    Counts the number of files with specified extensions in all subfolders of a given folder.

    :param folder_path: Path to the root folder containing raw documents.
    :param extensions: Set of file extensions to count (e.g., {".csv", ".pdf"}).
    :return: A dictionary with subfolder paths as keys and the number of matching files as values.
    :raises FileNotFoundError: If the folder_path does not exist.
    :raises PermissionError: If access to the folder is denied.
    """
    file_count_dict = {}

    try:
        # Walk through the directory structure
        for root, _, files in os.walk(folder_path):
            # Filter files by extension
            matching_files = [
                f for f in files if os.path.splitext(f)[1].lower() in extensions
            ]
            file_count_dict[root] = len(matching_files)
        return file_count_dict

    except FileNotFoundError:
        raise FileNotFoundError(f"The folder '{folder_path}' does not exist.")
    except PermissionError:
        raise PermissionError(f"Permission denied to access '{folder_path}'.")
    except Exception as e:
        raise Exception(f"An error occurred while counting files: {str(e)}")


def validate_documents_loaded(
    folder_path: str, df: pd.DataFrame, title_column: str = "page_title"
) -> Dict[str, any]:
    """
    Validates that all raw .csv and .pdf documents were loaded by comparing file count to unique titles in the DataFrame.

    :param folder_path: Path to the root folder containing raw documents.
    :param df: DataFrame output from the documents_loader pipeline.
    :param title_column: Column name in the DataFrame containing document titles (default: "page_title").
    :return: Dictionary with validation results.
    """
    # Count files with .csv and .pdf extensions
    file_counts = count_files_in_folder(folder_path, extensions={".csv", ".pdf"})
    total_raw_docs = sum(file_counts.values())

    # Get unique document titles from the DataFrame
    if title_column not in df.columns:
        raise ValueError(f"Column '{title_column}' not found in DataFrame.")

    unique_titles = df[title_column].nunique()
    missing_docs = total_raw_docs - unique_titles

    # Detailed report
    validation_result = {
        "total_raw_documents": total_raw_docs,
        "unique_loaded_titles": unique_titles,
        "missing_documents": missing_docs if missing_docs > 0 else 0,
        "extra_titles": -missing_docs if missing_docs < 0 else 0,
        "file_counts_by_folder": file_counts,
        "status": "PASS" if missing_docs == 0 else "FAIL",
        "message": (
            "All documents accounted for."
            if missing_docs == 0
            else f"{abs(missing_docs)} document(s) {'missing' if missing_docs > 0 else 'extra'} in DataFrame."
        ),
    }

    return validation_result


def main(folder_path: str = None, df: pd.DataFrame = None):
    """
    Main function to run validation, suitable for standalone testing or Kedro integration.

    :param folder_path: Path to raw documents folder (optional for testing).
    :param df: DataFrame from documents_loader (optional for testing).
    """
    # For standalone testing
    if folder_path is None:
        folder_path = input("Enter the path of the folder: ")
    if df is None:
        # Placeholder for testing; replace with actual DataFrame loading logic if needed
        print("No DataFrame provided. Please pass a DataFrame for validation.")
        return

    try:
        # Run validation
        result = validate_documents_loaded(folder_path, df)

        # Print results
        print("\nValidation Results:")
        print(f"Total raw .csv/.pdf documents: {result['total_raw_documents']}")
        print(f"Unique loaded document titles: {result['unique_loaded_titles']}")
        print(f"Missing documents: {result['missing_documents']}")
        print(f"Extra titles: {result['extra_titles']}")
        print(f"Status: {result['status']}")
        print(f"Message: {result['message']}")
        print("\nFile counts by subfolder:")
        for folder, count in result["file_counts_by_folder"].items():
            print(f"{folder}: {count} file(s)")

    except Exception as e:
        print(f"Error during validation: {str(e)}")

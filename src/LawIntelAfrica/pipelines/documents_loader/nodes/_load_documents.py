from langchain_community.document_loaders import PyPDFDirectoryLoader
import pandas as pd
import os
import pandas as pd
from docling.document_converter import DocumentConverter


def load_documents(data_path: str) -> pd.DataFrame:
    """
    Loads documents from all subfolders under the specified directory and returns them as a Pandas DataFrame.

    This function iterates over all subfolders in the given data_path, uses PyPDFDirectoryLoader to load documents
    from each subfolder, transform them into dataframes and concatenates them into a single DataFrame.

    Args:
        data_path (str): The path to the directory containing subfolders with documents.

    Returns:
        pd.DataFrame: A DataFrame containing all loaded documents from all subfolders.

    """
    docling_converter = DocumentConverter()
    
    dataframes = []
    for root, dirs, files in os.walk(data_path):
        if root == data_path:
            continue

        folder_name = os.path.basename(root).lower()
        if folder_name == "code":
            # Use PyPDFDirectoryLoader for the "code" folder
            document_loader = PyPDFDirectoryLoader(root)
            try:
                if documents := document_loader.load():
                    df = transform_to_page_df(documents, folder_name, root)
                    if not df.empty:
                        dataframes.append(df)
                        print(f"Folder converted: {root}")
            except Exception as e:
                print(f"Error processing folder {root}: {e}")
        else:
            for file in files:
                if file.lower().endswith(".pdf"):
                    file_path = os.path.join(root, file)
                    try:
                        result = docling_converter.convert(file_path)
                        
                        # Transform to page-by-page DataFrame
                        df = transform_to_page_df([], folder_name, file_path, docling_result=result.document)
                        if not df.empty:
                            dataframes.append(df)
                            print(f"File converted: {file_path}")
                    except Exception as e:
                        print(f"Error processing file {file_path}: {e}")

    if dataframes:
        return pd.concat(dataframes, ignore_index=True)
    else:
        print("No documents processed.")


def transform_to_page_df(documents, folder_name: str, source_path: str, docling_doc=None) -> pd.DataFrame:
    """Transform documents into a DataFrame with page-by-page content."""
    rows = []
    if docling_doc:
        content = docling_doc.export_to_text()
        rows.append({
            "folder": folder_name,
            "source": source_path,
            "page_label": 1,
            "text": content,
            "text_length": len(content.strip())
            
            
        })
    for doc in documents:
        # For PyPDFDirectoryLoader, each document is a page
        rows.append({
            "folder": folder_name,
            "source": doc.metadata["source"],
            "page_label": doc.metadata["page_label"],
            "text": doc.page_content,
            "text_length": len(doc.page_content.strip())
        })
    return pd.DataFrame(rows)
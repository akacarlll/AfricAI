from langchain_community.document_loaders import PyPDFDirectoryLoader
import pandas as pd
import os
import pytesseract
from pdf2image import convert_from_path
import pandas as pd

pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"
poppler_path = r"C:\Users\carlf\Downloads\poppler-24.08.0\Library\bin"


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
    dataframes = []
    for root, dirs, files in os.walk(data_path):
        if root == data_path:
            continue

        document_loader = PyPDFDirectoryLoader(root)
        # Load documents from the directory and transform them into a DataFrame if any exist
        if documents := document_loader.load():
            df = transform_list_to_df(documents)
            dataframes.append(df)
            print(f"Folder converted: {root}")

    if dataframes:
        combined_df = pd.concat(dataframes, ignore_index=True)
        return combined_df.apply(ocr_scanned_pdf, axis=1)
    else:
        print("Aucun document trouvé dans les sous-dossiers.")
        return pd.DataFrame()


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
        "text": page.page_content,
        "text_length": len(page.page_content.strip()),
    }

    for key, value in page.metadata.items():
        doc_dict[key] = value

    return doc_dict


def ocr_scanned_pdf(row):
    """
    Processes PDF pages with insufficient text content using OCR.
    Uses pdf2image to convert PDF pages to images and pytesseract for OCR.
    """

    if pd.isna(row["text"]) or len(str(row["text"])) < 200:
        try:
            # Convert the specific page to an image
            images = convert_from_path(
                row["source"],
                poppler_path=poppler_path,
                first_page=int(row["page"]) + 1,
                last_page=int(row["page"]) + 1,
                dpi=200,
            )

            if images:
                img = images[0]
                try:
                    ocr_text = pytesseract.image_to_string(img, lang="fra+eng")
                except:
                    # Fallback to English-only if language fails
                    ocr_text = pytesseract.image_to_string(img)
                row["text"] = ocr_text.strip()
                row["text_length"] = len(ocr_text)
            else:
                row["error"] = "No image generated"

        except Exception as e:
            print(f"Error processing {row['source']} page {row['page']}: {str(e)}")
            row["error"] = str(e)

    return row

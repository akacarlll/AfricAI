import gc
import io
import logging
import os
from collections import defaultdict
from pathlib import Path
import fitz
import pandas as pd
import pytesseract
from PIL import Image

logger = logging.getLogger(__name__)
pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"


def get_temp_filename(file_path: str, temp_folder: str = "temp") -> str:
    """
    Generate the expected temporary filename for a given file path.

    Args:
        file_path (str): Path to the original file.
        temp_folder (str): Folder where temporary files are stored (default: "temp").

    Returns:
        str: Path to the temporary CSV file.
    """
    base_name = os.path.basename(file_path)
    if base_name.lower().endswith(".pdf"):
        base_name = base_name[:-4]  # Remove .pdf extension
    temp_csv = f"temp_{base_name}.csv"
    return os.path.join(temp_folder, temp_csv)


def is_file_already_processed(file_path: str, temp_folder: str = "temp") -> bool:
    """
    Check if a file has already been processed by looking for its temporary CSV.

    Args:
        file_path (str): Path to the original file.
        temp_folder (str): Folder where temporary files are stored (default: "temp").

    Returns:
        bool: True if the temporary CSV exists, False otherwise.
    """
    expected_temp_file = get_temp_filename(file_path, temp_folder)
    return os.path.exists(expected_temp_file)


def process_document(
    file_path: str,
    folder_name: str,
    temp_folder: str,
    min_char_length: int = 50,
    ocr_language: str = "fra",
) -> str:
    """
    Extract text from PDF using PyMuPDF, with Tesseract OCR fallback for images.

    Args:
        file_path (str): Path to the PDF file.
        folder_name (str): Name of the folder containing the PDF.
        temp_folder (str): Folder to store temporary CSV files.
        min_char_length (int): Minimum character length to trigger OCR fallback (default: 50).
        ocr_language (str): Language for OCR (e.g., 'eng', 'spa', 'fra') (default: "fra").

    Returns:
        str: Basename of the temporary CSV file containing processed data.
    """
    doc_data = defaultdict(list)
    doc = fitz.open(file_path)

    for page_num in range(len(doc)):
        page = doc.load_page(page_num)
        page_text = page.get_text().strip()
        is_page_scanned = False

        if not page_text or len(page_text) < min_char_length:
            pix = page.get_pixmap(matrix=fitz.Matrix(2, 2))  # 2x scaling for better OCR
            img_data = pix.tobytes("png")

            img = Image.open(io.BytesIO(img_data))

            ocr_text = pytesseract.image_to_string(img, lang=ocr_language)
            page_text = ocr_text.strip()
            is_page_scanned = True

        doc_data["page_number"].append(page_num + 1)
        doc_data["page_content"].append(page_text)
        doc_data["text_length"].append(len(page_text.strip()))
        doc_data["is_page_scanned"].append(is_page_scanned)

    doc.close()

    document_parsed_in_df = pd.DataFrame(doc_data)
    document_parsed_in_df["folder"] = folder_name
    document_parsed_in_df["source"] = file_path
    document_parsed_in_df["file_type"] = "pdf"

    temp_csv = f"temp_{os.path.basename(file_path).replace('.pdf', '')}.csv"
    document_parsed_in_df.to_csv(os.path.join(temp_folder, temp_csv), index=False)

    save_message = f"Saved processed results to {temp_csv}"
    logger.info(save_message)

    assert os.path.exists(os.path.join(temp_folder, temp_csv))

    return os.path.basename(os.path.join(temp_folder, temp_csv))


def read_csvs(processed_files: list[str]):
    """Reads CSV files in chunks and yields the rows.

    Args:
        processed_files (list[str]): List of paths to processed CSV files.

    Yields:
        pd.DataFrame: Chunks of the CSV file as DataFrames.
    """
    for file in processed_files:
        try:
            yield from pd.read_csv(file, chunksize=1000)
        except Exception as e:
            error_message = f"Error reading {file}: {e}"
            logger.error(error_message)


def load_documents(data_path:dict, country: str) -> pd.DataFrame:
    """
    Load and process PDF documents from a directory, combining results into a DataFrame.

    Args:
        data_path (dict): Dictionary containing paths to the directories for each country.
        country (str): The country for which the documents are being loaded.

    Returns:
        pd.DataFrame: Combined DataFrame of processed documents, or empty if none processed.
    """
    temp_folder = "temp_documents"
    if not os.path.exists(temp_folder):
        os.makedirs(temp_folder)

    processed_files = [
        file
        for file in os.listdir(temp_folder)
        if file.startswith("temp_") and file.endswith(".csv")
    ]
    processed_files_message = (
        f"Found {len(processed_files)} already processed files in temp folder"
    )
    logger.info(processed_files_message)
    processed_files = [os.path.join(temp_folder, f) for f in processed_files]

    for root, dirs, files in os.walk(data_path[country]):
        if root == data_path[country]:
            continue

        folder_name = os.path.basename(root).lower()
        files_to_process = []

        for file in files:
            if file.lower().endswith(".pdf"):
                file_path = os.path.join(root, file)
                if not is_file_already_processed(file_path, temp_folder):
                    files_to_process.append(file)
                else:
                    temp_csv = os.path.basename(
                        get_temp_filename(file_path, temp_folder)
                    )
                    temp_csv_path = os.path.join(temp_folder, temp_csv)
                    if temp_csv_path not in processed_files:
                        processed_files.append(temp_csv_path)
                        already_processed_message = (
                            f"File {file} already processed. Added to results list."
                        )
                        logger.info(already_processed_message)

        files_to_process_message = (
            f"Found {len(files_to_process)} files that need processing in {root}"
        )
        logger.info(files_to_process_message)

        for file in files_to_process:
            file_path = os.path.join(root, file)
            csv_path = process_document(file_path, folder_name, temp_folder)
            if csv_path:
                csv_full_path = os.path.join(temp_folder, csv_path)
                processed_files.append(csv_full_path)

        gc.collect()

    combine_message = "Combining processed files..."
    logger.info(combine_message)

    result_df = pd.concat(read_csvs(processed_files), ignore_index=True)

    # Uncomment if you want the file to be deleted automatically.
    for file in processed_files:
        os.remove(file)

    return result_df

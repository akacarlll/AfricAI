import csv
from urllib.parse import unquote
import re
import csv
import unicodedata


def get_page_title(title: str) -> str:
    """
    Generates a file name from a page title, with intelligent truncation.

    Arguments:
    - title (str): The page title.

    Returns:
    - cleaned_title (str): The adapted file name.
    """
    decoded_title = unquote(title)
    special_chars = r"[^\w\s]"
    cleaned_title = re.sub(special_chars, "_", decoded_title)

    normalized_title = unicodedata.normalize("NFKD", cleaned_title)
    cleaned_title = "".join(
        [c for c in normalized_title if not unicodedata.combining(c)]
    )

    cleaned_title = cleaned_title.replace(" ", "_")
    cleaned_title = cleaned_title.rstrip("_")
    cleaned_title = re.sub("_+", "_", cleaned_title)

    return cleaned_title


def generate_file_name(text: str, max_length: int = 120) -> str:
    """
    Extracts a file name from text by identifying year patterns.

    Searches for 4-digit numbers that look like years (1900-2100) in the text.
    If at least two valid years are found, truncates the text to include up to
    and including the second year occurrence.

    Args:
        text (str): The input text to process.

    Returns:
        str: The processed text, either truncated at the second year if found,
             or the original text if fewer than two valid years are detected.
    """
    text = text.upper()
    numbers = re.findall(r"\d{4}", text)
    years = [num for num in numbers if 1900 <= int(num) <= 2100]

    if len(years) >= 2:
        second_year = years[1]
        split_index = text.rfind(second_year) + len(second_year)
        text = text[:split_index]

    if len(text) > max_length:
        last_underscore = text[:max_length].rfind("_")
        if last_underscore != -1:
            text = text[:last_underscore]
        else:
            text = text[:max_length]

    return text


def categorize_file(file_name: str) -> str:
    file_name = file_name.lower()
    category = "autres"  # Par défaut
    if "decret" in file_name:
        category = "decret"
    elif "arrete" in file_name:
        category = "arrete"
    elif "circulaire" in file_name:
        category = "circulaire"
    elif "loi" in file_name:
        category = "loi"
    elif re.search(r"\barret\b|arret[^a-zA-Z]", file_name):
        category = "arret"
    return category


def save_file(
    file_path: str,
    url: str,
    text: str,
    title_on_page: str,
    page_label: int = 0,
    category: str = None,
    metadata: dict = None,
) -> None:

    with open(file_path, mode="w", newline="", encoding="utf-8") as csv_file:
        writer = csv.writer(csv_file)
        writer.writerow(
            ["URL", "text", "page_title", "page_label", "category", "metadata"]
        )
        writer.writerow([url, text, title_on_page, page_label, category, metadata])

    print(f"Text extracted and added to file: {file_path}")

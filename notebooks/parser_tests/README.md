# README: PDF Parser Comparison Notebook

## Overview


The primary aim of this notebook is to parse and analyze a subset of PDF files, specifically focusing on scanned PDFs, which constitute approximately 500 files or 12% of the total documents.
This Jupyter Notebook script (`test_parser.ipynb`) is designed to compare the performance of various PDF parsing libraries on a set of scanned and digital PDF documents. It evaluates parsers based on success rate, extraction time, and text quality, generating a detailed HTML report with results and recommendations.

The script supports both text-based (digital) and image-based (scanned) PDFs, using a mix of native text extraction tools and OCR (Optical Character Recognition) libraries. It’s optimized for use in a Jupyter Notebook environment but can be adapted for standalone execution.

## Features

**Parsers Tested:**

-   `pdfplumber`: High-level text and table extraction.
-   `pypdf`: Simple text extraction from digital PDFs.
-   `pytesseract`: OCR for scanned PDFs (requires Tesseract).
-   `easyocr`: OCR alternative for scanned PDFs.
-   `pymupdf (MuPDF)`: Fast text extraction from digital PDFs.

**Metrics:**

-   Success rate (% of files successfully parsed).
-   Average processing time (seconds).
-   Text quality (character count, word count, line count).

**Output:**

-   Raw results in JSON (`pdf_parser_results.json`).
-   Analyzed data in JSON (`pdf_parser_analysis.json`).
-   Performance table in CSV (`parser_performance.csv`).
-   HTML report (`pdf_parser_report.html`) with summary, tables, and recommendations.
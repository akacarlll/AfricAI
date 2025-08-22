# AfricAI

## Description
AfricAI is a project aimed at collecting, processing, and leveraging legal data from various websites across multiple African countries. Using Kedro to orchestrate data processing pipelines, AfricAI builds a searchable knowledge base that can power a RAG (Retrieval-Augmented Generation) system or an Agentic-System.

## Objectifs
- Scrape legal data in multiple formats (PDF, scanned images, plain text, etc.).
- Extract and process information using a Kedro pipeline.
- Load and analyze documents (text extraction, table and image parsing, data parsing).
- Preprocess data (segmentation, text cleaning, redundancy removal, normalization).
- Build vector databases (ChromaDB, Faiss, Qdrant).

## Architecture
AfricAI is built on a modular and scalable architecture:

1. Data Collection: Scraping legal websites and downloading documents.
2. Extraction & Processing: Using PyPDFLoader and OCR tools to extract text and tables.
3. Preprocessing: Cleaning and normalizing the data.
4. Storage: Indexing data in ChromaDB with embeddings for fast retrieval.


## Project Installation
```bash
git clone https://github.com/akacarlll/AfricAI.git
cd Africai

```  
## Install dependencies
```  
conda env create -f environment.yml
```

## Launch the project
Currently, only Cameroonian legal documents are available.
To scrape data, use the following commands:

**Scrape the data from [juriafrica](https://www.juriafrica.com/)**
```
python src\scraping_bots\cmr_bots\scraping_juriafrica\main.py
```  

  
**Scrape the data from [spm_gov.com](https://www.spm.gov.cm/)**
```src\scraping_bots\cmr_bots\scraping_bots_spm_gov\main.py
```  
## Run the the pipelines:
You have several options to launch the pipelines:
Run the all the Kedro pipelines:  
```kedro run```
This will execute all pipelines, from loading documents to creating vector stores.

Run a single pipeline:
```kedro run --pipeline=xxx```
Replace xxx with the name of the pipeline you want to run.
## Technologies utilisées
- **Kedro** : Data pipeline orchestration.
- **ChromaDB** : Embedding storage and indexing.
- **OCR & NLP** : Document extraction and processing.
- **LangChain** : Conversational agent construction.

## Contribution
Contributions are welcome! Feel free to open an issue or submit a pull request.



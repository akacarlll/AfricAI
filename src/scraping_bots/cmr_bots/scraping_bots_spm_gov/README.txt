**What this bot does:**

This bot is designed to scrape legal documents from one of the official website of Cameroon’s government, 'spm.gov.cm' 
This sites contains a large majority of Decreets, Orders (Presidential, Ministerial, Administrative) and Communiqués.
It follows these main steps:

1. **URL Extraction:**  
   The bot navigates through different pages of the government’s legal documentation section, collecting all URLs pointing to individual law pages or downloadable PDF documents.

2. **Page Type Detection:**  
   For each collected URL, the bot determines whether the page primarily contains downloadable PDFs or text-based content.

3. **Content Retrieval:**  
   - **Text Pages:** The bot extracts the relevant text, often from `<p>` tags or similar HTML elements, and stores it in CSV files.  
   - **PDF Pages:** The bot downloads the linked PDF files and saves them for further analysis.

4. **File Organization:**  
   The extracted text and downloaded PDFs are stored in organized directories, making it easy to access raw data for further processing.
   They are stored in data/01_raw/spm_cm_data
5. **Iterative Process:**  
   The bot continuously iterates over multiple pages until it detects that no more content is available, ensuring that all relevant documents are captured.

**Purpose:**  
This bot serves as a foundational data collection tool for building a Retrieval-Augmented Generation (RAG) pipeline. It prepares raw legal data, which can later be processed, indexed, and used in applications requiring quick retrieval of relevant legal information.
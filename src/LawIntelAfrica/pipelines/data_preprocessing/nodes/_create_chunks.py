import pandas as pd
from nltk.tokenize import sent_tokenize

def chunk_text(df, chunk_size, chunk_overlap=0, method='fixed', sentence_tokenizer_language='english'):
    """
    Chunk a DataFrame containing text documents for RAG applications.
    
    Parameters:
        df (pd.DataFrame): Input DataFrame with columns ['text', 'document_name', 'page_label']
        chunk_size (int): Maximum size of chunks (in characters)
        chunk_overlap (int): Overlap between chunks for 'sliding' method (default 0)
        method (str): Chunking method - 'fixed', 'sliding', or 'sentence' (default 'fixed')
        sentence_tokenizer_language (str): Language for sentence tokenization (default 'english')
    
    Returns:
        pd.DataFrame: New DataFrame with chunked text and preserved metadata
    """
    df['text'] = df['text'].fillna("")
    
    # Validate inputs
    if chunk_size <= 0:
        raise ValueError("chunk_size must be greater than 0")
    if method not in ['fixed', 'sliding', 'sentence']:
        raise ValueError("Method must be 'fixed', 'sliding', or 'sentence'")
    if method == 'sliding' and chunk_overlap >= chunk_size:
        raise ValueError("chunk_overlap must be smaller than chunk_size for sliding method")
    
    # Handle NLTK punkt installation for sentence tokenization
    if method == 'sentence':
        try:
            sent_tokenize("test", language=sentence_tokenizer_language)
        except LookupError:
            import nltk
            nltk.download('punkt')
    
    chunks = []
    
    for _, row in df.iterrows():
        text = row['text']
        doc_name = row['document_name']
        page = row['page_label']
        
        if method == 'fixed':
            start = 0
            while start < len(text):
                end = start + chunk_size
                chunks.append({
                    'text': text[start:end],
                    'document_name': doc_name,
                    'page_label': page
                })
                start += chunk_size
                
        elif method == 'sliding':
            step = chunk_size - chunk_overlap
            start = 0
            while start < len(text):
                end = start + chunk_size
                chunks.append({
                    'text': text[start:end],
                    'document_name': doc_name,
                    'page_label': page
                })
                start += step
                
        elif method == 'sentence':
            sentences = sent_tokenize(text, language=sentence_tokenizer_language)
            current_chunk = []
            current_length = 0
            
            for sent in sentences:
                sent_len = len(sent)
                space_len = 1 if current_chunk else 0  # Account for space between sentences
                
                if current_length + space_len + sent_len > chunk_size:
                    if current_chunk:
                        chunks.append({
                            'text': ' '.join(current_chunk),
                            'document_name': doc_name,
                            'page_label': page
                        })
                        current_chunk = []
                        current_length = 0
                        
                current_chunk.append(sent)
                current_length += space_len + sent_len
                
            if current_chunk:  # Add remaining sentences
                chunks.append({
                    'text': ' '.join(current_chunk),
                    'document_name': doc_name,
                    'page_label': page
                })
    
    return pd.DataFrame(chunks)
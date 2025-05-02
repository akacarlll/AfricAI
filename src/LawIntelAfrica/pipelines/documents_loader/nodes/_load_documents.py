from langchain_community.document_loaders import PyPDFDirectoryLoader
import pandas as pd
import os
import time
from tqdm import tqdm
import gc
import psutil
from docling.document_converter import DocumentConverter, PdfFormatOption
from docling.datamodel.pipeline_options import PdfPipelineOptions, AcceleratorDevice, AcceleratorOptions
from docling.datamodel.base_models import InputFormat
import sys

try :
    import resource
except ImportError:
    pass
pipeline_options = PdfPipelineOptions()
pipeline_options.do_ocr = True
pipeline_options.do_table_structure = False
pipeline_options.enable_remote_services = False
pipeline_options.artifacts_path = r"C:\Users\carlf\Documents\GitHub\docling-models"
pipeline_options.accelerator_options = AcceleratorOptions(
    num_threads=max(1, os.cpu_count() // 2),
    device=AcceleratorDevice.CPU,
)

docling_converter = DocumentConverter(
    format_options={
        InputFormat.PDF: PdfFormatOption(pipeline_options=pipeline_options)
    }
)

def print_memory_usage(label=""):
    process = psutil.Process(os.getpid())
    memory_mb = process.memory_info().rss / 1024 / 1024
    print(f"Memory usage {label}: {memory_mb:.2f} MB")

def transform_to_page_df(documents, folder_name: str, source_path: str, docling_doc=None) -> pd.DataFrame:
    if docling_doc:
        content = docling_doc.export_to_text()
        df = pd.DataFrame([{
            "folder": folder_name,
            "source": source_path,
            "page_label": 1,
            "text": content,
            "text_length": len(content.strip())
        }])
        del content
        return df
    
    if documents:
        return pd.DataFrame([{
            "folder": folder_name,
            "source": doc.metadata["source"],
            "page_label": doc.metadata["page_label"],
            "text": doc.page_content,
            "text_length": len(doc.page_content.strip())
        } for doc in documents])
    
    return pd.DataFrame()
def get_temp_filename(file_path, temp_folder="temp"):
    """Generate the expected temp filename for a given file path"""
    base_name = os.path.basename(file_path)
    if base_name.lower().endswith(".pdf"):
        base_name = base_name[:-4]  # Remove .pdf extension
    temp_csv = f"temp_{base_name}.csv"
    return os.path.join(temp_folder, temp_csv)

def is_file_already_processed(file_path, temp_folder="temp"):
    """Check if a file has already been processed by looking for its temp CSV"""
    expected_temp_file = get_temp_filename(file_path, temp_folder)
    return os.path.exists(expected_temp_file)

def process_single_file(file_path, folder_name, temp_folder="temp"):
    print_memory_usage(f"before processing {os.path.basename(file_path)}")
    
    try:
        start_time = time.time()
        
        result = docling_converter.convert(file_path)
        
        end_time = time.time() - start_time
        print(f"Time taken to convert {file_path}: {end_time:.2f} seconds")
        
        temp_csv = f"temp_{os.path.basename(file_path).replace('.pdf', '')}.csv"
        
        df = transform_to_page_df([], folder_name, file_path, result.document)
        
        if not df.empty:
            df.to_csv(os.path.join(temp_folder, temp_csv), index=False)
            print(f"Saved processed results to {temp_csv}")
        
        del df
        del result
        
        gc.collect()
        print_memory_usage(f"after processing {os.path.basename(file_path)}")
        
        time.sleep(3)
        
        return temp_csv if os.path.exists(temp_csv) else None
        
    except Exception as e:
        print(f"Error processing file {file_path}: {e}")
        return None

def load_documents(data_path: str) -> pd.DataFrame:

    if sys.platform != "win32":
        try:
            resource.setrlimit(resource.RLIMIT_AS, (4 * 1024 * 1024 * 1024, -1))
        except (ValueError, OSError):
            pass
    temp_folder = "temp"
    if not os.path.exists(temp_folder):
        os.makedirs(temp_folder)
        
    processed_files = [f for f in os.listdir(temp_folder) if f.startswith("temp_") and f.endswith(".csv")]
    print(f"Found {len(processed_files)} already processed files in temp folder")
    processed_files = [os.path.join(temp_folder, f) for f in processed_files]
    
    for root, dirs, files in os.walk(data_path):
        if root == data_path:
            continue

        folder_name = os.path.basename(root).lower()
        
        if folder_name == "code":
            document_loader = PyPDFDirectoryLoader(root)
            try:
                if documents := document_loader.load():
                    temp_csv = f"temp_{folder_name}_{os.path.basename(root)}.csv"
                    
                    df = transform_to_page_df(documents, folder_name, root)
                    if not df.empty:
                        df.to_csv(os.path.join(temp_folder, temp_csv), index=False)
                        processed_files.append(temp_csv)
                        print(f"Folder converted: {root}")
                    
                    del df
                    del documents
                    gc.collect()
            except Exception as e:
                print(f"Error processing folder {root}: {e}")
        else:
            batch_size = 5
            files_to_process = []
            for file in files:
                if file.lower().endswith(".pdf"):
                    file_path = os.path.join(root, file)
                    if not is_file_already_processed(file_path, temp_folder):
                        files_to_process.append(file)
                    else:
                        temp_csv = os.path.basename(get_temp_filename(file_path, temp_folder))
                        temp_csv_path = os.path.join(temp_folder, temp_csv)
                        if temp_csv_path not in processed_files:
                            processed_files.append(temp_csv_path)
                            print(f"File {file} already processed. Added to results list.")
            
            print(f"Found {len(files_to_process)} files that need processing in {root}")
            
            file_batches = [files_to_process[i:i+batch_size] for i in range(0, len(files_to_process), batch_size)]
            
            for batch in file_batches:
                for file in tqdm(batch):
                    file_path = os.path.join(root, file)
                    csv_path = process_single_file(file_path, folder_name, temp_folder)
                    if csv_path:
                        csv_full_path = os.path.join(temp_folder, csv_path)
                        if csv_full_path not in processed_files:
                            processed_files.append(csv_full_path)
                
                gc.collect()
                time.sleep(30)
                print_memory_usage("after batch")

    if processed_files:
        print("Combining processed files...")
        
        def read_csvs():
            for file in processed_files:
                try:
                    for chunk in pd.read_csv(file, chunksize=1000):
                        yield chunk
                except Exception as e:
                    print(f"Error reading {file}: {e}")
        
        try:
            result_df = pd.concat(read_csvs(), ignore_index=True)
            
            for file in processed_files:
                try:
                    os.remove(file)
                except:
                    pass
                    
            return result_df
        except Exception as e:
            print(f"Error combining results: {e}")
            return pd.DataFrame()
    else:
        print("No documents processed.")
        return pd.DataFrame()
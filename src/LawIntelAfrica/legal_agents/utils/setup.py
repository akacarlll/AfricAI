from langchain.llms import HuggingFacePipeline
from langchain.embeddings import HuggingFaceEmbeddings
from transformers import AutoModelForCausalLM, AutoTokenizer, pipeline
from config import MODEL_NAME, EMBEDDING_MODEL
# Setup LLM
def setup_llm():
    """Set up the language model for agents."""
    tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME)
    model = AutoModelForCausalLM.from_pretrained(MODEL_NAME, device_map="auto")
    
    pipe = pipeline(
        "text-generation",
        model=model,
        tokenizer=tokenizer,
        max_length=512,
        temperature=0.1,
        top_p=0.95,
        repetition_penalty=1.15
    )
    
    return HuggingFacePipeline(pipeline=pipe)

# Setup embeddings
def setup_embeddings():
    """Set up the embedding model."""
    return HuggingFaceEmbeddings(model_name=EMBEDDING_MODEL)
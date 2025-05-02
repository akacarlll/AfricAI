from langchain.llms import HuggingFacePipeline
from langchain_community.embeddings import HuggingFaceEmbeddings
from transformers import AutoModelForCausalLM, AutoTokenizer, pipeline
from src.LawIntelAfrica.legal_agents.config import MODEL_DIR, LLM_DIR, EMBEDDING_DIR
import os

import shutil
from transformers import AutoModelForCausalLM, AutoTokenizer
from sentence_transformers import SentenceTransformer


# Assurez-vous que les répertoires existent
os.makedirs(MODEL_DIR, exist_ok=True)


def download_models():
    """Télécharge les modèles s'ils n'existent pas déjà localement."""
    # Télécharger le modèle de langage
    print(f"Checking LLM_DIR: {LLM_DIR}")
    model_file = os.path.join(LLM_DIR, "pytorch_model.bin")
    if not os.path.exists(LLM_DIR) or not os.path.exists(model_file):
        print(f"Téléchargement du modèle LLM 'databricks/dolly-v2-3b'...")
        try:
            # Clear the directory if it exists
            if os.path.exists(LLM_DIR):
                shutil.rmtree(LLM_DIR)
            os.makedirs(LLM_DIR, exist_ok=True)

            # Download tokenizer and model
            tokenizer = AutoTokenizer.from_pretrained("databricks/dolly-v2-3b")
            model = AutoModelForCausalLM.from_pretrained("databricks/dolly-v2-3b")

            # Save to LLM_DIR
            tokenizer.save_pretrained(LLM_DIR)
            model.save_pretrained(LLM_DIR)
            print("Modèle LLM téléchargé et sauvegardé.")

            # Verify the model weights file exists
            if not os.path.exists(model_file):
                raise FileNotFoundError(
                    f"Model weights file {model_file} not found after saving!"
                )
            print(f"Verified: Model weights file exists at {model_file}")
        except Exception as e:
            print(f"Erreur lors du téléchargement ou de la sauvegarde du LLM : {e}")
            raise

    # Télécharger le modèle d'embeddings
    print(f"Checking EMBEDDING_DIR: {EMBEDDING_DIR}")
    embedding_file = os.path.join(EMBEDDING_DIR, "model.safetensors")
    if not os.path.exists(EMBEDDING_DIR) or not os.path.exists(embedding_file):
        print(
            f"Téléchargement du modèle d'embeddings 'sentence-transformers/all-MiniLM-L6-v2'..."
        )
        try:
            model = SentenceTransformer("sentence-transformers/all-MiniLM-L6-v2")
            os.makedirs(EMBEDDING_DIR, exist_ok=True)
            model.save(EMBEDDING_DIR)
            print("Modèle d'embeddings téléchargé et sauvegardé.")
        except Exception as e:
            print(
                f"Erreur lors du téléchargement ou de la sauvegarde des embeddings : {e}"
            )
            raise


# Modifier les fonctions setup pour utiliser les modèles locaux
def setup_llm():
    """Set up the language model for agents."""
    tokenizer = AutoTokenizer.from_pretrained(LLM_DIR)
    model = AutoModelForCausalLM.from_pretrained(LLM_DIR, device_map="auto")

    pipe = pipeline(
        "text-generation",
        model=model,
        tokenizer=tokenizer,
        max_length=512,
        temperature=0.1,
        top_p=0.95,
        repetition_penalty=1.15,
    )

    return HuggingFacePipeline(pipeline=pipe)


def setup_embeddings():
    """Set up the embedding model."""
    return HuggingFaceEmbeddings(model_name=EMBEDDING_DIR)

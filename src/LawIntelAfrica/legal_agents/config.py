column validator hookimport os

# Database paths
CHROMA_PATH_1 = r"C:\Users\carlf\Documents\GitHub\LawIntelAfrica\data\chroma"

# Définir des chemins locaux pour les modèles
MODEL_DIR = os.path.join(os.path.dirname(__file__), "models")
LLM_DIR = os.path.join(MODEL_DIR, "dolly-v2-3b")
EMBEDDING_DIR = os.path.join(MODEL_DIR, "all-MiniLM-L6-v2")

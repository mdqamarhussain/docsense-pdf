from dotenv import load_dotenv
import os

load_dotenv()

QDRANT_URL = os.getenv("QDRANT_URL", "http://localhost:6333")
COLLECTION_NAME = os.getenv("COLLECTION_NAME", "documents")
OLLAMA_MODEL = os.getenv("OLLAMA_MODEL", "llama3.2:3b")
TEMPERATURE = float(os.getenv("TEMPERATURE", 0))
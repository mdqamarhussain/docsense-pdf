from langchain_qdrant import QdrantVectorStore
from app.core.config import COLLECTION_NAME, QDRANT_URL
from app.services.embeddings import get_embeddings


def get_vector_store() -> QdrantVectorStore:
    return QdrantVectorStore.from_existing_collection(
        collection_name=COLLECTION_NAME,
        url=QDRANT_URL,
        embedding=get_embeddings(),
    )
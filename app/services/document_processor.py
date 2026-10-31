from pathlib import Path
from shutil import copyfileobj

from fastapi import UploadFile
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_qdrant import QdrantVectorStore
from qdrant_client import QdrantClient

from app.core.config import COLLECTION_NAME, QDRANT_URL
from app.services.embeddings import get_embeddings


def process_pdf(file: UploadFile, file_path: Path) -> dict[str, int | str]:
    with file_path.open("wb") as buffer:
        copyfileobj(file.file, buffer)

    loader = PyPDFLoader(str(file_path))
    docs = loader.load()


    splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=400
    )

    chunks = splitter.split_documents(docs)

    for chunk in chunks:
        chunk.metadata["file_name"] = file.filename

    client = QdrantClient(url=QDRANT_URL)
    embedding_model = get_embeddings()
    if client.collection_exists(COLLECTION_NAME):
        vector_store = QdrantVectorStore.from_existing_collection(
            collection_name=COLLECTION_NAME,
            url=QDRANT_URL,
            embedding=embedding_model,
        )
        vector_store.add_documents(chunks)
    else:
        QdrantVectorStore.from_documents(
            documents=chunks,
            embedding=embedding_model,
            collection_name=COLLECTION_NAME,
            url=QDRANT_URL,
        )

    return {
        "message": "PDF uploaded successfully",
        "file_name": file.filename or file_path.name,
        "pages": len(docs),
        "chunks": len(chunks),
    }
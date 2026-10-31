from langchain_community.embeddings import FastEmbedEmbeddings
from langchain_core.embeddings import Embeddings


def get_embeddings() -> Embeddings:
    return FastEmbedEmbeddings(
        model_name="BAAI/bge-small-en-v1.5"
    )
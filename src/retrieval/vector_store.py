"""
Initialises and manages the ChromaDB vector store.
"""
import os
from langchain_chroma import Chroma
from langchain_community.embeddings import HuggingFaceEmbeddings
from retrieval.document_loader import load_kb_documents
from retrieval.chunking import chunk_documents

PERSIST_DIR = os.getenv("CHROMA_PERSIST_DIR", "./outputs/chroma_db")
COLLECTION = os.getenv("VECTOR_STORE_COLLECTION", "support_kb")


def get_vector_store() -> Chroma:
    embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")

    if os.path.exists(PERSIST_DIR):
        return Chroma(
            collection_name=COLLECTION,
            embedding_function=embeddings,
            persist_directory=PERSIST_DIR,
        )

    docs = load_kb_documents()
    chunks = chunk_documents(docs)
    store = Chroma.from_documents(
        documents=chunks,
        embedding=embeddings,
        collection_name=COLLECTION,
        persist_directory=PERSIST_DIR,
    )
    return store

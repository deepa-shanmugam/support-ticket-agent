"""
Retriever: wraps the vector store for similarity search.
"""
from retrieval.vector_store import get_vector_store
from langchain_core.documents import Document


class Retriever:
    def __init__(self):
        self._store = get_vector_store()

    def retrieve(self, query: str, top_k: int = 5) -> list[Document]:
        return self._store.similarity_search(query, k=top_k)

"""
Loads knowledge base Markdown documents for ingestion into the vector store.
"""
import os
from langchain_community.document_loaders import DirectoryLoader, TextLoader
from langchain_core.documents import Document


KB_DIR = os.path.join(os.path.dirname(__file__), "../../data/knowledge_base")


def load_kb_documents() -> list[Document]:
    loader = DirectoryLoader(
        KB_DIR,
        glob="**/*.md",
        loader_cls=TextLoader,
        loader_kwargs={"encoding": "utf-8"},
    )
    docs = loader.load()
    for doc in docs:
        doc.metadata["source"] = os.path.basename(doc.metadata.get("source", "unknown"))
    return docs

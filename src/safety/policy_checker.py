"""
Policy checker: verifies whether a relevant policy exists in the knowledge base.
"""
from retrieval.retriever import Retriever


class PolicyChecker:
    def __init__(self):
        self.retriever = Retriever()

    def check(self, ticket: dict) -> tuple[list[str], bool]:
        docs = self.retriever.retrieve(ticket["message"], top_k=3)
        if not docs:
            return [], False
        sources = list({d.metadata.get("source", "unknown") for d in docs})
        return sources, True

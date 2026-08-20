"""
RAG agent: retrieves relevant KB documents and drafts a reply.
"""
from langchain_groq import ChatGroq
from retrieval.retriever import Retriever


class RAGAgent:
    def __init__(self):
        self.retriever = Retriever()
        self.llm = ChatGroq(model="llama-3.1-8b-instant", temperature=0.2)

    def draft_reply(self, ticket: dict, sources: list[str], retry: int = 0) -> tuple[str, float]:
        docs = self.retriever.retrieve(ticket["message"], top_k=5 + retry)

        context = "\n\n".join([d.page_content for d in docs])
        source_names = [d.metadata.get("source", "unknown") for d in docs]

        prompt = f"""You are a customer support agent. Using ONLY the policy information below, draft a helpful reply to the customer ticket.
If the policy does not cover the situation, say so explicitly.

TICKET:
Subject: {ticket['subject']}
Message: {ticket['message']}

POLICY CONTEXT:
{context}

Draft a concise, empathetic reply. Do not fabricate policies not found above."""

        response = self.llm.invoke(prompt)
        draft = response.content

        confidence = self._score_confidence(draft, context, retry)
        return draft, confidence

    def _score_confidence(self, draft: str, context: str, retry: int) -> float:
        if not context.strip():
            return 0.30
        overlap = sum(1 for word in draft.lower().split() if word in context.lower())
        base = min(0.95, 0.50 + (overlap / max(len(draft.split()), 1)) * 0.5)
        return max(0.30, base - retry * 0.05)

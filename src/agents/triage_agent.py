"""
Triage agent: decides routing based on sentiment, policy, and confidence.
"""
from utils.constants import (
    ROUTE_AUTO_RESOLVE, ROUTE_ESCALATE, ROUTE_REFUSE, ROUTE_ASK_MORE_INFO
)


class TriageAgent:
    def decide(self, sentiment: str, policy_found: bool, confidence: float, ticket: dict) -> str:
        if sentiment == "abusive":
            return ROUTE_REFUSE

        if not policy_found:
            return ROUTE_ESCALATE

        history = ticket.get("conversation_history", [])
        if self._is_repeated_refund(ticket, history):
            return ROUTE_ESCALATE

        if confidence >= 0.85:
            return ROUTE_AUTO_RESOLVE

        if confidence < 0.50:
            return ROUTE_ESCALATE

        required = self._missing_required_fields(ticket)
        if required:
            return ROUTE_ASK_MORE_INFO

        return ROUTE_AUTO_RESOLVE

    def _is_repeated_refund(self, ticket: dict, history: list) -> bool:
        if ticket.get("category") != "refund_request":
            return False
        return len(history) > 0

    def _missing_required_fields(self, ticket: dict) -> list[str]:
        missing = []
        if not ticket.get("customer_id"):
            missing.append("customer_id")
        if not ticket.get("message"):
            missing.append("message")
        return missing

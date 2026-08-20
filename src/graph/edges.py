"""
LangGraph edge routing logic for the support ticket agent.
"""
from utils.constants import (
    ROUTE_AUTO_RESOLVE, ROUTE_ESCALATE, ROUTE_REFUSE, ROUTE_ASK_MORE_INFO
)


def route_after_decision(state: dict) -> str:
    route = state.get("route_decision", "")
    if route == ROUTE_REFUSE:
        return "refuse"
    if route == ROUTE_ESCALATE:
        return "hitl_approval"
    if route == ROUTE_ASK_MORE_INFO:
        return "hitl_approval"
    return "confidence_recheck_or_hitl"


def route_after_confidence_recheck(state: dict) -> str:
    """Loop back for another retrieval pass or proceed to HITL."""
    confidence = state.get("confidence_score", 0.0)
    retry_count = state.get("retry_count", 0)
    max_retries = 3

    if confidence >= 0.85 or retry_count >= max_retries:
        return "hitl_approval"
    return "confidence_recheck"


def route_after_hitl(state: dict) -> str:
    action = state.get("reviewer_action", "PENDING")
    if action == "APPROVED" or action == "ESCALATE":
        return "save_draft"
    if action == "REGENERATE":
        return "rag_draft"
    if action == "REJECTED":
        return "refuse"
    return "save_draft"

"""
LangGraph state definition for the support ticket agent.
"""
from typing import TypedDict, Optional, Annotated
from langgraph.graph.message import add_messages


class GraphState(TypedDict):
    ticket: dict
    sentiment: str
    policy_found: bool
    retrieved_sources: list[str]
    draft_reply: str
    route_decision: str
    confidence_score: float
    retry_count: int
    reviewer_action: Optional[str]
    reviewer_comments: Optional[str]
    audit_entry: Optional[dict]
    messages: Annotated[list, add_messages]

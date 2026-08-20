"""
Pydantic schemas for tickets, draft replies, and audit entries.
"""
from pydantic import BaseModel, Field
from typing import Optional


class ConversationTurn(BaseModel):
    role: str
    message: str
    timestamp: str = ""


class Ticket(BaseModel):
    ticket_id: str
    customer_id: str
    subject: str
    message: str
    conversation_history: list[ConversationTurn] = Field(default_factory=list)
    priority: str = "medium"
    category: str = ""
    created_at: str = ""


class DraftReply(BaseModel):
    ticket_id: str
    draft_reply: str
    route_decision: str
    confidence_score: float
    retrieved_sources: list[str] = Field(default_factory=list)
    reviewer_action: Optional[str] = None
    reviewer_comments: Optional[str] = None


class AuditEntry(BaseModel):
    ticket_id: str
    route_decision: str
    confidence_score: float
    sentiment: str
    policy_found: bool
    retrieved_sources: list[str]
    reviewer_action: Optional[str]
    reviewer_comments: Optional[str]
    logged_at: str

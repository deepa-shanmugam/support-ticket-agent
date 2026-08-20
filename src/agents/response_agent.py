"""
Response agent: finalises and formats the draft reply for HITL review.
"""
import json
import os
from utils.schemas import DraftReply

DRAFT_REPLIES_DIR = os.getenv("DRAFT_REPLIES_DIR", "./outputs/drafted_replies")


class ResponseAgent:
    def __init__(self):
        os.makedirs(DRAFT_REPLIES_DIR, exist_ok=True)

    def format_draft(self, ticket: dict, draft: str, route: str, confidence: float, sources: list[str]) -> DraftReply:
        reply = DraftReply(
            ticket_id=ticket["ticket_id"],
            draft_reply=draft,
            route_decision=route,
            confidence_score=round(confidence, 4),
            retrieved_sources=sources,
        )
        path = os.path.join(DRAFT_REPLIES_DIR, f"{ticket['ticket_id']}.json")
        with open(path, "w") as f:
            json.dump(reply.model_dump(), f, indent=2)
        return reply

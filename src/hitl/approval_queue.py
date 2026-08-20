"""
Approval queue: holds drafted replies pending human reviewer action.
"""
import json
import os
from datetime import datetime
from langgraph.types import interrupt
from utils.constants import CONFIDENCE_HITL_AUTO_APPROVE

HITL_QUEUE_DIR = os.getenv("HITL_QUEUE_DIR", "./outputs/hitl_queue")


class ApprovalQueue:
    def __init__(self):
        self._queue: list[dict] = []
        os.makedirs(HITL_QUEUE_DIR, exist_ok=True)

    def submit(self, state: dict) -> dict:
        entry = {
            "ticket_id": state["ticket"]["ticket_id"],
            "draft_reply": state.get("draft_reply", ""),
            "route_decision": state.get("route_decision", ""),
            "confidence_score": state.get("confidence_score", 0.0),
            "retrieved_sources": state.get("retrieved_sources", []),
            "submitted_at": datetime.utcnow().isoformat(),
            "reviewer_action": "PENDING",
            "reviewer_comments": "",
            "status": "PENDING",
        }
        self._queue.append(entry)

        if entry["confidence_score"] >= CONFIDENCE_HITL_AUTO_APPROVE:
            entry["reviewer_action"] = "APPROVED"
            entry["reviewer_comments"] = "Auto-approved: high confidence."
            entry["status"] = "REVIEWED"
            return entry

        path = os.path.join(HITL_QUEUE_DIR, f"{entry['ticket_id']}.json")
        with open(path, "w") as f:
            json.dump(entry, f, indent=2)

        reviewed = interrupt(entry)
        reviewed["status"] = "REVIEWED"
        path2 = os.path.join(HITL_QUEUE_DIR, f"{entry['ticket_id']}.json")
        with open(path2, "w") as f:
            json.dump(reviewed, f, indent=2)
        return reviewed

    def get_queue(self) -> list[dict]:
        return list(self._queue)

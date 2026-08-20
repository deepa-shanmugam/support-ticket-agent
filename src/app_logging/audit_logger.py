"""
Audit logger: writes immutable audit entries for every ticket processed.
"""
import json
import os
from datetime import datetime

AUDIT_LOG_DIR = os.getenv("AUDIT_LOG_DIR", "./outputs/audit_logs")


class AuditLogger:
    def __init__(self):
        os.makedirs(AUDIT_LOG_DIR, exist_ok=True)

    def log(self, ticket_id: str, state: dict) -> None:
        entry = {
            "ticket_id": ticket_id,
            "route_decision": state.get("route_decision"),
            "confidence_score": state.get("confidence_score"),
            "sentiment": state.get("sentiment"),
            "policy_found": state.get("policy_found"),
            "retrieved_sources": state.get("retrieved_sources", []),
            "reviewer_action": state.get("reviewer_action"),
            "reviewer_comments": state.get("reviewer_comments"),
            "logged_at": datetime.utcnow().isoformat(),
        }
        path = os.path.join(AUDIT_LOG_DIR, f"{ticket_id}.json")
        with open(path, "w") as f:
            json.dump(entry, f, indent=2)

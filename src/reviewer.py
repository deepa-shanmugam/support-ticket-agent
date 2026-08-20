"""
Standalone HITL reviewer script.

Usage:
    python src/reviewer.py

Reads all PENDING tickets from outputs/hitl_queue/, prompts the reviewer
for each, then resumes the paused graph threads with the decisions.
"""
import json
import os
import glob
from dotenv import load_dotenv

load_dotenv()

from langgraph.types import Command
from graph.support_graph import build_support_graph, CHECKPOINT_DB
from hitl.approval_ui_stub import prompt_reviewer

HITL_QUEUE_DIR = os.getenv("HITL_QUEUE_DIR", "./outputs/hitl_queue")


def load_pending() -> list[dict]:
    pattern = os.path.join(HITL_QUEUE_DIR, "*.json")
    entries = []
    for path in sorted(glob.glob(pattern)):
        with open(path) as f:
            entry = json.load(f)
        if entry.get("status") == "PENDING":
            entries.append(entry)
    return entries


def main():
    pending = load_pending()
    if not pending:
        print("No pending HITL tickets found.")
        return

    print(f"Found {len(pending)} ticket(s) awaiting review.\n")
    graph = build_support_graph()

    for entry in pending:
        reviewed = prompt_reviewer(entry)
        config = {"configurable": {"thread_id": entry["ticket_id"]}}
        result = graph.invoke(Command(resume=reviewed), config=config)

        state = graph.get_state(config)
        status = "COMPLETE" if not state.next else "STILL PENDING"
        print(f"  {entry['ticket_id']}: {reviewed['reviewer_action']} — {status}")

    print("\nReview complete.")


if __name__ == "__main__":
    main()

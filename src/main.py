"""
Entry point for the Support Ticket Triage & Resolution Agent.
"""
import json
import os
from dotenv import load_dotenv

load_dotenv()

from graph.support_graph import build_support_graph
from utils.schemas import Ticket


def load_tickets(path: str) -> list[Ticket]:
    with open(path, "r") as f:
        raw = json.load(f)
    return [Ticket(**t) for t in raw]


def main():
    tickets = load_tickets("data/tickets/synthetic_tickets.json")
    graph = build_support_graph()
    pending_hitl = []

    for ticket in tickets:
        config = {"configurable": {"thread_id": ticket.ticket_id}}
        print(f"\nProcessing {ticket.ticket_id}: {ticket.subject}")
        result = graph.invoke({"ticket": ticket.model_dump()}, config=config)

        state = graph.get_state(config)
        if state.next:
            pending_hitl.append(ticket.ticket_id)
            print(f"  Route: {result.get('route_decision', '?')}")
            print(f"  Confidence: {result.get('confidence_score', 0):.2f}")
            print(f"  HITL Status: PENDING — queued for human review")
        else:
            print(f"  Route: {result.get('route_decision')}")
            print(f"  Confidence: {result.get('confidence_score', 0):.2f}")
            print(f"  HITL Status: {result.get('reviewer_action', 'N/A')}")

    if pending_hitl:
        print(f"\n{len(pending_hitl)} ticket(s) queued for HITL review: {', '.join(pending_hitl)}")
        print("Run:  python src/reviewer.py")


if __name__ == "__main__":
    main()

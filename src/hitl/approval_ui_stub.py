"""
Stub UI for HITL approval — simulates a reviewer interface in the terminal.
"""
from hitl.reviewer_actions import ReviewerActions

reviewer = ReviewerActions()


def prompt_reviewer(entry: dict) -> dict:
    print("\n" + "=" * 60)
    print(f"TICKET: {entry['ticket_id']}")
    print(f"ROUTE:  {entry['route_decision']}  (confidence: {entry['confidence_score']:.2f})")
    print(f"SOURCES: {', '.join(entry.get('retrieved_sources', []))}")
    print("\nDRAFT REPLY:")
    print(entry["draft_reply"])
    print("=" * 60)
    print("Actions: [A]pprove  [R]eject  [G]enerate again  [E]scalate")

    choice = input("Reviewer action: ").strip().upper()
    comments = input("Comments (optional): ").strip()

    action_map = {"A": "APPROVED", "R": "REJECTED", "G": "REGENERATE", "E": "ESCALATE"}
    action = action_map.get(choice, "PENDING")
    return reviewer.apply(entry, action, comments)

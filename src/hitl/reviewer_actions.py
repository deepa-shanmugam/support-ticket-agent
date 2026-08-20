"""
Reviewer action handler: processes decisions made by human reviewers.
"""
from utils.constants import REVIEWER_ACTIONS


class ReviewerActions:
    VALID_ACTIONS = REVIEWER_ACTIONS

    def apply(self, entry: dict, action: str, comments: str = "") -> dict:
        if action not in self.VALID_ACTIONS:
            raise ValueError(f"Invalid reviewer action: {action}. Must be one of {self.VALID_ACTIONS}")
        entry["reviewer_action"] = action
        entry["reviewer_comments"] = comments
        return entry

    def approve(self, entry: dict, comments: str = "") -> dict:
        return self.apply(entry, "APPROVED", comments)

    def reject(self, entry: dict, comments: str = "") -> dict:
        return self.apply(entry, "REJECTED", comments)

    def request_regeneration(self, entry: dict, comments: str = "") -> dict:
        return self.apply(entry, "REGENERATE", comments)

    def escalate(self, entry: dict, comments: str = "") -> dict:
        return self.apply(entry, "ESCALATE", comments)

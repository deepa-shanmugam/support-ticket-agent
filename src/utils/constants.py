"""
Application-wide constants.
"""

ROUTE_AUTO_RESOLVE = "AUTO_RESOLVE"
ROUTE_ESCALATE = "ESCALATE"
ROUTE_REFUSE = "REFUSE"
ROUTE_ASK_MORE_INFO = "ASK_FOR_MORE_INFO"

ALL_ROUTES = [ROUTE_AUTO_RESOLVE, ROUTE_ESCALATE, ROUTE_REFUSE, ROUTE_ASK_MORE_INFO]

REVIEWER_ACTIONS = ["APPROVED", "REJECTED", "REGENERATE", "ESCALATE", "PENDING"]

SENTIMENT_LABELS = ["positive", "neutral", "negative", "abusive"]

TICKET_CATEGORIES = [
    "refund_request",
    "subscription_cancellation",
    "login_access_issue",
    "product_troubleshooting",
    "abusive_message",
    "billing_issue",
]

CONFIDENCE_AUTO_RESOLVE = 0.85
CONFIDENCE_ESCALATE = 0.50
CONFIDENCE_HITL_AUTO_APPROVE = 0.95
MAX_RETRY_LOOPS = 3
REFUND_WINDOW_DAYS = 7
REFUND_ABUSE_WINDOW_DAYS = 90

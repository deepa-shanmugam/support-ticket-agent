"""
Scripted refusal response templates.
"""

ABUSIVE_REFUSAL = (
    "Thank you for reaching out. We want to help resolve your issue, but we're unable to assist "
    "when messages contain threatening or abusive language. Please contact us again when you are "
    "ready to communicate respectfully, and we will be happy to help."
)

POLICY_VIOLATION_REFUSAL = (
    "We appreciate you contacting us. Unfortunately, we are unable to process this request as it "
    "falls outside our service policies. If you believe this is an error, please contact us with "
    "additional context and we'll be glad to review."
)

FRAUD_REFUSAL = (
    "We take the security of all accounts seriously. This request has been flagged for review and "
    "has been escalated to our Trust & Safety team. You will be contacted if further information "
    "is needed."
)


def get_refusal_message(sentiment: str = "abusive") -> str:
    if sentiment == "abusive":
        return ABUSIVE_REFUSAL
    return POLICY_VIOLATION_REFUSAL

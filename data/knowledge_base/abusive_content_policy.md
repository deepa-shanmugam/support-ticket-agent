# Abusive Content Policy

## Zero-Tolerance Policy

We are committed to providing a respectful experience for both customers and support staff. Abusive, threatening, or harassing communication will not be tolerated.

## Definition of Abusive Content

The following are considered abusive and will trigger an automatic refusal response:

- **Threatening language**: Threats of harm, legal threats made in bad faith, or threats to damage reputation.
- **Hate speech**: Language targeting individuals based on race, gender, religion, nationality, or other protected characteristics.
- **Harassment**: Repeated aggressive or hostile messages directed at support staff.
- **Profanity and personal attacks**: Excessive use of profanity or personal insults directed at staff.

## Agent Response Protocol

When a ticket is classified as containing abusive content:

1. Do **not** engage with the abusive content.
2. Send the scripted refusal response (see `refusal_templates.py`).
3. Log the ticket with an `ABUSIVE_CONTENT` flag in the audit log.
4. Escalate to the Trust & Safety team if threats are credible or repeated.

## Scripted Refusal Message

> "Thank you for reaching out. We want to help resolve your issue, but we're unable to assist when messages contain threatening or abusive language. Please contact us again when you are ready to communicate respectfully, and we will be happy to help."

## Important Note for Agents

Agents must **never** respond in kind to abusive messages. The scripted refusal is the only approved response. Do not attempt to resolve the underlying issue in the same interaction.

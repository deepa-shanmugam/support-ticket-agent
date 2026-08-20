"""
Sentiment agent: classifies the sentiment of an incoming ticket message.
"""
from langchain_groq import ChatGroq


SENTIMENT_LABELS = ["positive", "neutral", "negative", "abusive"]


class SentimentAgent:
    def __init__(self):
        self.llm = ChatGroq(model="llama-3.1-8b-instant", temperature=0.0)

    def analyze(self, message: str) -> str:
        prompt = f"""Classify the sentiment of the following customer support message.
Choose exactly one label from: {SENTIMENT_LABELS}

- "abusive": threatening, harassing, or contains hate speech
- "negative": frustrated or upset but not abusive
- "neutral": matter-of-fact inquiry
- "positive": satisfied or complimentary

Message: {message}

Reply with only the label."""

        response = self.llm.invoke(prompt)
        label = response.content.strip().lower()
        return label if label in SENTIMENT_LABELS else "neutral"

"""
Abuse detection: identifies abusive, threatening, or harassing content.
"""
import re

ABUSE_PATTERNS = [
    r"\b(kill|destroy|threaten|hack|sue|lawyer)\b",
    r"\b(idiot|stupid|useless|criminal|thief|scam)\b",
    r"[!]{3,}",
]


class AbuseDetector:
    def __init__(self):
        self._patterns = [re.compile(p, re.IGNORECASE) for p in ABUSE_PATTERNS]

    def is_abusive(self, text: str) -> bool:
        return any(p.search(text) for p in self._patterns)

    def score(self, text: str) -> float:
        hits = sum(1 for p in self._patterns if p.search(text))
        return min(1.0, hits / len(self._patterns))

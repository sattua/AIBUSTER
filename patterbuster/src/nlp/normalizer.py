# src/nlp/normalizer.py

from textblob import TextBlob
import logging
import re

logger = logging.getLogger(__name__)

def looks_like_code_block(text: str):
    return (
        "\n" in text and
        any(sym in text for sym in [";", "{", "}", "SELECT", "function", "<script"])
    )

def is_question(text: str):
    return any(q in text for q in ["how", "what", "why", "does", "can", "?"])

EXECUTION_HINTS = [
    "run this",
    "execute this",
    "try this",
    "paste this",
    "use this command"
]

def has_execution_intent(text: str):
    return any(h in text for h in EXECUTION_HINTS)

def normalize_text(text: str) -> str:
    text = text.lower().strip()
    text = re.sub(r"[^a-z0-9\s]", "", text)

    blob = TextBlob(text)
    corrected = str(blob.correct())

    print(f"normalize (corrected): {corrected}")

    return corrected
# src/nlp/normalizer.py

from textblob import TextBlob
import re

def normalize_text(text: str) -> str:
    text = text.lower().strip()
    text = re.sub(r"[^a-z0-9\s]", "", text)

    blob = TextBlob(text)
    return str(blob.correct())
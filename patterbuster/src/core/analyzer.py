# src/core/analyzer.py

import re
import logging

from src.nlp.normalizer import (
    normalize_text,
    looks_like_code_block,
    is_question,
    has_execution_intent
)

logger = logging.getLogger(__name__)

INJECTION_ACTIONS = [
    "ignore", "disregard", "bypass", "override"
]

INJECTION_TARGETS = [
    "instructions", "rules", "restrictions", "guidelines", "safety"
]

INJECTION_PATTERNS = [
    "act as .* without"
]

# base sensitive terms (singular only, avoid duplication)
BASE_SENSITIVE_TERMS = [
    "key",
    "password",
    "secret",
    "token"
]

# extended sensitive targets (derived, no duplication)
SENSITIVE_TARGETS = list(set(
    BASE_SENSITIVE_TERMS +
    [
        "api key",
        "credentials",
        "database",
        "data"
    ]
))

PATTERNS = {
    "prompt_injection": {
        "weight": 0.5,
        "patterns": INJECTION_PATTERNS
    },
    "sensitive_request": {
        "weight": 0.7,
        "patterns": [
            rf"\b{term}s?\b" for term in BASE_SENSITIVE_TERMS
        ]
    }
}

SUSPICIOUS_ACTIONS = [
    "give", "show", "send", "dump", "export", "reveal", "provide"
]

def split_sentences(text: str):
    return re.split(r"[.,;!?]", text.lower())

def close_match(sentence, actions, targets, max_distance=5):
    words = sentence.split()
    for i, word in enumerate(words):
        if word in actions:
            for j in range(max(0, i - max_distance), min(len(words), i + max_distance)):
                if words[j] in targets:
                    return True
    return False

def detect_prompt_injection(sentence: str, max_distance=5):
    words = sentence.split()

    for i, word in enumerate(words):
        if word in INJECTION_ACTIONS:
            for j in range(max(0, i - max_distance), min(len(words), i + max_distance)):
                if words[j] in INJECTION_TARGETS:
                    pattern = rf"{word}.*?{words[j]}"
                    match = re.search(pattern, sentence)
                    if match:
                        return match
    return None

def detect_data_exfiltration(sentence: str, max_distance=5):
    words = sentence.split()

    for i, word in enumerate(words):
        if word in SUSPICIOUS_ACTIONS:
            for j in range(max(0, i - max_distance), min(len(words), i + max_distance)):
                if words[j] in SENSITIVE_TARGETS:
                    pattern = rf"{word}.*?{words[j]}"
                    match = re.search(pattern, sentence)
                    if match:
                        return match
    return None

class Finding:
    def __init__(self, f_type, sentence, match_text=None, start=None, end=None):
        self.type = f_type
        self.sentence = sentence
        self.match = match_text
        self.start = start
        self.end = end

    def key(self):
        return (self.type, self.sentence, self.start, self.end)

    def to_dict(self):
        return {
            "type": self.type,
            "sentence": self.sentence,
            "match": self.match,
            "start": self.start,
            "end": self.end
        }

def analyze_prompt(text: str):
    normalized_text = normalize_text(text)

    is_code = looks_like_code_block(text)
    question = is_question(text)
    execution_intent = has_execution_intent(text)

    sentences = split_sentences(normalized_text)
    findings = []
    seen = set()
    total_score = 0

    def add_finding(f_type, sentence, match_text=None, start=None, end=None):
        finding = Finding(f_type, sentence, match_text, start, end)
        key = finding.key()
        if key not in seen:
            # TODO refactor: encapsulate findings structure.
            seen.add(key)
            findings.append(finding.to_dict())

    for sentence in sentences:
        sentence = sentence.strip()
        if not sentence:
            continue

        sentence_score = 0

        # Pattern-based detection (con índices)
        for category, config in PATTERNS.items():
            for pattern in config["patterns"]:
                for match in re.finditer(pattern, sentence, re.IGNORECASE):
                    add_finding(
                        category,
                        sentence,
                        match.group(),
                        match.start(),
                        match.end()
                    )
                    sentence_score = max(sentence_score, config["weight"])

        # Dynamic prompt injection
        injection_match = detect_prompt_injection(sentence)
        if injection_match:
            add_finding(
                "prompt_injection",
                sentence,
                injection_match.group(),
                injection_match.start(),
                injection_match.end()
            )
            sentence_score = max(sentence_score, 0.5)

        # Heurística básica
        action_found = any(a in sentence for a in SUSPICIOUS_ACTIONS)
        target_found = any(t in sentence for t in SENSITIVE_TARGETS)

        if action_found and target_found:
            for match in re.finditer(rf"\b({'|'.join(SUSPICIOUS_ACTIONS)})\b", sentence):
                add_finding(
                    "sensitive_access_attempt",
                    sentence,
                    match.group(),
                    match.start(),
                    match.end()
                )
            sentence_score = max(sentence_score, 0.8)

        elif target_found:
            for match in re.finditer(rf"\b({'|'.join(SENSITIVE_TARGETS)})\b", sentence):
                add_finding(
                    "sensitive_reference",
                    sentence,
                    match.group(),
                    match.start(),
                    match.end()
                )
            sentence_score = max(sentence_score, 0.4)

        # Contextual
        if close_match(sentence, SUSPICIOUS_ACTIONS, SENSITIVE_TARGETS):
            add_finding("contextual_sensitive_attempt", sentence)
            sentence_score = max(sentence_score, 0.85)

        # Data exfiltration con match
        exfil_match = detect_data_exfiltration(sentence)
        if exfil_match:
            add_finding(
                "data_exfiltration",
                sentence,
                exfil_match.group(),
                exfil_match.start(),
                exfil_match.end()
            )
            sentence_score = max(sentence_score, 0.9)

        # context-aware adjustment
        if is_code and question and not execution_intent:
            add_finding("code_context", sentence)
            sentence_score *= 0.3

        if execution_intent:
            add_finding("execution_intent", sentence)
            sentence_score = max(sentence_score, 0.9)

        total_score += sentence_score

    risk_score = total_score / len(sentences) if sentences else 0

    return {
        "riskScore": min(round(risk_score, 2), 1.0),
        "findings": findings
    }
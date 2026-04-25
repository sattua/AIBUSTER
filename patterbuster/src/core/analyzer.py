# src/core/analyzer.py

import re
import logging

logger = logging.getLogger(__name__)

PATTERNS = {
    "prompt_injection": {
        "weight": 0.5,
        "patterns": [
            r"ignore previous instructions",
            r"disregard.*rules",
            r"act as .* without restrictions"
        ]
    },
    "sensitive_request": {
        "weight": 0.7,
        "patterns": [
            r"api key",
            r"password",
            r"secret",
            r"token"
        ]
    },
    "data_exfiltration": {
        "weight": 0.9,
        "patterns": [
            r"show me all",
            r"dump database",
            r"export data"
        ]
    }
}

SUSPICIOUS_ACTIONS = ["give", "show", "send", "dump", "export", "reveal"]
SENSITIVE_TARGETS = ["api key", "api keys", "password", "token", "secret"]

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

def analyze_prompt(text: str):
    logger.info(f"analyze_prompt Starts: {text}")

    sentences = split_sentences(text)
    findings = []
    total_score = 0

    for sentence in sentences:
        sentence = sentence.strip()

        # 🔹 Pattern-based detection
        for category, config in PATTERNS.items():
            for pattern in config["patterns"]:
                if re.search(pattern, sentence):
                    findings.append({
                        "type": category,
                        "sentence": sentence
                    })
                    total_score += config["weight"]

        # 🔹 Heuristic detection
        action_found = any(a in sentence for a in SUSPICIOUS_ACTIONS)
        target_found = any(t in sentence for t in SENSITIVE_TARGETS)

        if action_found and target_found:
            findings.append({
                "type": "sensitive_access_attempt",
                "sentence": sentence
            })
            total_score += 0.8

        elif target_found:
            findings.append({
                "type": "sensitive_reference",
                "sentence": sentence
            })
            total_score += 0.4

        # 🔹 Contextual detection
        if close_match(sentence, SUSPICIOUS_ACTIONS, SENSITIVE_TARGETS):
            findings.append({
                "type": "contextual_sensitive_attempt",
                "sentence": sentence
            })
            total_score += 0.85

    logger.info(f"analyze_prompt ends: Score:{total_score}, findings {findings}")

    return {
        "risk_score": min(round(total_score, 2), 1.0),
        "findings": findings
    }
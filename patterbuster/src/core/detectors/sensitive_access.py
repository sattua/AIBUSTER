import re
from typing import List

from src.core.detectors.base import Detector
from src.core.findings import Finding


class SensitiveAccessDetector(Detector):
    base_sensitive_terms = ["key", "password", "secret", "token"]
    sensitive_targets = [
        "key",
        "password",
        "secret",
        "token",
        "api key",
        "credentials",
        "database",
        "data",
    ]
    suspicious_actions = ["give", "show", "send", "dump", "export", "reveal", "provide"]
    sensitive_request_score = 0.7
    reference_score = 0.4
    access_attempt_score = 0.8
    contextual_score = 0.85

    def detect(self, sentence: str) -> List[Finding]:
        findings: List[Finding] = []

        for term in self.base_sensitive_terms:
            pattern = rf"\b{term}s?\b"
            for match in re.finditer(pattern, sentence):
                findings.append(
                    Finding(
                        "sensitive_request",
                        sentence,
                        match.group(),
                        match.start(),
                        match.end(),
                        score=self.sensitive_request_score,
                    )
                )

        action_found = any(a in sentence for a in self.suspicious_actions)
        target_found = any(t in sentence for t in self.sensitive_targets)

        if action_found and target_found:
            action_pattern = rf"\b({'|'.join(self.suspicious_actions)})\b"
            for match in re.finditer(action_pattern, sentence):
                findings.append(
                    Finding(
                        "sensitive_access_attempt",
                        sentence,
                        match.group(),
                        match.start(),
                        match.end(),
                        score=self.access_attempt_score,
                    )
                )
        elif target_found:
            target_pattern = rf"\b({'|'.join(self.sensitive_targets)})\b"
            for match in re.finditer(target_pattern, sentence):
                findings.append(
                    Finding(
                        "sensitive_reference",
                        sentence,
                        match.group(),
                        match.start(),
                        match.end(),
                        score=self.reference_score,
                    )
                )

        if self._close_match(sentence):
            findings.append(
                Finding(
                    "contextual_sensitive_attempt",
                    sentence,
                    score=self.contextual_score,
                )
            )

        return findings

    def _close_match(self, sentence: str, max_distance: int = 5) -> bool:
        words = sentence.split()

        for i, word in enumerate(words):
            if word in self.suspicious_actions:
                for j in range(max(0, i - max_distance), min(len(words), i + max_distance)):
                    if words[j] in self.sensitive_targets:
                        return True

        return False

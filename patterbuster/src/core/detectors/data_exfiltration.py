import re
from typing import List

from src.core.detectors.base import Detector
from src.core.findings import Finding


class DataExfiltrationDetector(Detector):
    suspicious_actions = ["give", "show", "send", "dump", "export", "reveal", "provide"]
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
    score = 0.9

    def detect(self, sentence: str) -> List[Finding]:
        findings: List[Finding] = []
        words = sentence.split()
        max_distance = 5

        for i, word in enumerate(words):
            if word in self.suspicious_actions:
                for j in range(max(0, i - max_distance), min(len(words), i + max_distance)):
                    if words[j] in self.sensitive_targets:
                        pattern = rf"{word}.*?{words[j]}"
                        match = re.search(pattern, sentence)
                        if match:
                            findings.append(
                                Finding(
                                    "data_exfiltration",
                                    sentence,
                                    match.group(),
                                    match.start(),
                                    match.end(),
                                    score=self.score,
                                )
                            )

        return findings

import re
from typing import List

from src.core.detectors.base import Detector
from src.core.findings import Finding


class PromptInjectionDetector(Detector):
    actions = ["ignore", "disregard", "bypass", "override"]
    targets = ["instructions", "rules", "restrictions", "guidelines", "safety"]
    patterns = [r"act as .* without"]
    score = 0.5

    def detect(self, sentence: str) -> List[Finding]:
        findings: List[Finding] = []

        for pattern in self.patterns:
            for match in re.finditer(pattern, sentence, re.IGNORECASE):
                findings.append(
                    Finding(
                        "prompt_injection",
                        sentence,
                        match.group(),
                        match.start(),
                        match.end(),
                        score=self.score,
                    )
                )

        words = sentence.split()
        max_distance = 5

        for i, word in enumerate(words):
            if word in self.actions:
                for j in range(max(0, i - max_distance), min(len(words), i + max_distance)):
                    if words[j] in self.targets:
                        pattern = rf"{word}.*?{words[j]}"
                        match = re.search(pattern, sentence)
                        if match:
                            findings.append(
                                Finding(
                                    "prompt_injection",
                                    sentence,
                                    match.group(),
                                    match.start(),
                                    match.end(),
                                    score=self.score,
                                )
                            )

        return findings

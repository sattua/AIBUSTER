# src/core/analyzer.py

import logging
from typing import List

from src.core.detectors import (
    DataExfiltrationDetector,
    PromptInjectionDetector,
    SensitiveAccessDetector,
)
from src.core.findings import AnalysisResult, Finding
from src.core.normalizer import Normalizer
from src.core.risk_scorer import RiskScorer
from src.core.sentence_splitter import SentenceSplitter

logger = logging.getLogger(__name__)


class Analyzer:
    def __init__(
        self,
        detectors: List = None,
        normalizer: Normalizer = None,
        splitter: SentenceSplitter = None,
        scorer: RiskScorer = None,
    ):
        self.normalizer = normalizer or Normalizer()
        self.splitter = splitter or SentenceSplitter()
        self.detectors = detectors or [
            PromptInjectionDetector(),
            DataExfiltrationDetector(),
            SensitiveAccessDetector(),
        ]
        self.scorer = scorer or RiskScorer()

    def analyze(self, text: str) -> AnalysisResult:
        normalized_text = self.normalizer.normalize(text)

        is_code = self.normalizer.looks_like_code_block(text)
        question = self.normalizer.is_question(text)
        execution_intent = self.normalizer.has_execution_intent(text)

        sentences = self.splitter.split(normalized_text)
        findings: List[Finding] = []
        seen = set()
        sentence_scores: List[float] = []

        for sentence in sentences:
            sentence = sentence.strip()
            if not sentence:
                sentence_scores.append(0.0)
                continue

            sentence_score = 0.0

            for detector in self.detectors:
                for finding in detector.detect(sentence):
                    if finding.key() not in seen:
                        seen.add(finding.key())
                        findings.append(finding)
                    sentence_score = max(sentence_score, finding.score or 0.0)

            if is_code and question and not execution_intent:
                code_context = Finding("code_context", sentence)
                if code_context.key() not in seen:
                    seen.add(code_context.key())
                    findings.append(code_context)
                sentence_score *= 0.3

            if execution_intent:
                execution_finding = Finding("execution_intent", sentence, score=0.9)
                if execution_finding.key() not in seen:
                    seen.add(execution_finding.key())
                    findings.append(execution_finding)
                sentence_score = max(sentence_score, 0.9)

            sentence_scores.append(sentence_score)

        risk_score = self.scorer.calculate(sentence_scores, len(sentences))
        return AnalysisResult(risk_score, findings)


def analyze_prompt(text: str):
    analyzer = Analyzer()
    return analyzer.analyze(text).to_dict()

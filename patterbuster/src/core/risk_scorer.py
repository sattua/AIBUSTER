from typing import List


class RiskScorer:
    def calculate(self, sentence_scores: List[float], sentence_count: int) -> float:
        if sentence_count == 0:
            return 0.0

        total_score = sum(sentence_scores)
        return min(round(total_score / sentence_count, 2), 1.0)

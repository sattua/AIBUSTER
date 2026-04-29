from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional


@dataclass
class Finding:
    type: str
    sentence: str
    match: Optional[str] = None
    start: Optional[int] = None
    end: Optional[int] = None
    score: Optional[float] = None

    def key(self) -> tuple:
        return (self.type, self.sentence, self.start, self.end)

    def to_dict(self) -> Dict[str, Any]:
        data: Dict[str, Any] = {
            "type": self.type,
            "sentence": self.sentence,
        }

        if self.match is not None:
            data["match"] = self.match
        if self.start is not None:
            data["start"] = self.start
        if self.end is not None:
            data["end"] = self.end

        return data


@dataclass
class AnalysisResult:
    risk_score: float
    findings: List[Finding] = field(default_factory=list)

    def to_dict(self) -> Dict[str, Any]:
        return {
            "riskScore": min(round(self.risk_score, 2), 1.0),
            "findings": [finding.to_dict() for finding in self.findings]
        }

from abc import ABC, abstractmethod
from typing import List

from src.core.findings import Finding


class Detector(ABC):
    @abstractmethod
    def detect(self, sentence: str) -> List[Finding]:
        raise NotImplementedError

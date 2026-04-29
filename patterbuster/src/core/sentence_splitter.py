import re
from typing import List


class SentenceSplitter:
    def split(self, text: str) -> List[str]:
        return re.split(r"[.,;!?]", text.lower())

from src.nlp.normalizer import (
    normalize_text,
    looks_like_code_block,
    is_question,
    has_execution_intent
)


class Normalizer:
    def normalize(self, text: str) -> str:
        return normalize_text(text)

    def looks_like_code_block(self, text: str) -> bool:
        return looks_like_code_block(text)

    def is_question(self, text: str) -> bool:
        return is_question(text)

    def has_execution_intent(self, text: str) -> bool:
        return has_execution_intent(text)

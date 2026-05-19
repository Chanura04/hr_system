import re
from typing import List

from app.services.openai_client import OpenAIClient


class EmbeddingService:

    def __init__(self):
        self.client = OpenAIClient()

    def embed(self, text: str) -> List[float]:
        try:
            return self.client.embed(text)
        except Exception:
            return self._local_embed(text)

    @staticmethod
    def _local_embed(text: str) -> List[float]:
        tokens = re.findall(r"\w+", text.lower())
        counts = {}
        for token in tokens:
            if len(token) < 2:
                continue
            counts[token] = counts.get(token, 0) + 1

        vocabulary = [
            "scheduling", "meeting", "leave", "vacation", "compliance",
            "policy", "training", "manager", "salary", "urgent",
            "request", "approve", "cancel", "book", "travel",
            "holiday", "time", "off", "help", "clarify"
        ]

        length = max(sum(counts.values()), 1)
        return [counts.get(word, 0) / length for word in vocabulary]

    @staticmethod
    def cosine_similarity(vector_a: List[float], vector_b: List[float]) -> float:
        dot_product = sum(a * b for a, b in zip(vector_a, vector_b))
        norm_a = sum(a * a for a in vector_a) ** 0.5
        norm_b = sum(b * b for b in vector_b) ** 0.5

        if norm_a == 0 or norm_b == 0:
            return 0.0

        return dot_product / (norm_a * norm_b)

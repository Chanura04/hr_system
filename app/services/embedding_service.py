import re
from typing import List

from app.config import settings
from app.services.openai_client import OpenAIClient


class EmbeddingService:

    # def __init__(self):
    #     self.client = OpenAIClient()
    #     self.embedding_dim = 1536

    # def embed(self, text: str) -> List[float]:
    #     try:
    #         return self.client.embed(text)
    #     except Exception:
    #         return self._local_embed(text)

    # def _local_embed(self, text: str) -> List[float]:
    #     tokens = re.findall(r"\w+", text.lower())
    #     counts = {}
    #     for token in tokens:
    #         if len(token) < 2:
    #             continue
    #         idx = abs(hash(token)) % self.embedding_dim
    #         counts[idx] = counts.get(idx, 0) + 1

    #     vector = [counts.get(i, 0) for i in range(self.embedding_dim)]
    #     norm = sum(value * value for value in vector) ** 0.5
    #     if norm == 0:
    #         return vector

    #     return [value / norm for value in vector]

    # @staticmethod
    # def cosine_similarity(vector_a: List[float], vector_b: List[float]) -> float:
    #     dot_product = sum(a * b for a, b in zip(vector_a, vector_b))
    #     norm_a = sum(a * a for a in vector_a) ** 0.5
    #     norm_b = sum(b * b for b in vector_b) ** 0.5

    #     if norm_a == 0 or norm_b == 0:
    #         return 0.0

    #     return dot_product / (norm_a * norm_b)
    pass

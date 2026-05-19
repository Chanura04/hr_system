from typing import Dict, List

from openai import OpenAI

from app.config import settings


class OpenAIClient:
    def __init__(self):
        if not settings.OPENAI_API_KEY:
            raise ValueError("OPENAI_API_KEY is required for LLM and embeddings services.")

        base_url = settings.OPENAI_BASE_URL.rstrip("/")
        self.client = OpenAI(
            api_key=settings.OPENAI_API_KEY,
            base_url=base_url
        )
        self.model = settings.MODEL_NAME or "gpt-4o-mini"
        self.embedding_model = settings.EMBEDDING_MODEL_NAME or "text-embedding-3-small"

    def chat(self, messages: List[Dict[str, str]], temperature: float = 0.0, max_tokens: int = 300) -> str:
        response = self.client.chat.completions.create(
            model=self.model,
            messages=messages,
            temperature=temperature,
            max_tokens=max_tokens,
        )

        return response.choices[0].message.content.strip()

    def embed(self, text: str) -> List[float]:
        response = self.client.embeddings.create(
            model=self.embedding_model,
            input=text
        )
        return response.data[0].embedding

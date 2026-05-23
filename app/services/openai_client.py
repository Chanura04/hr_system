from typing import Dict, List

from openai import OpenAI

from app.config import settings
from app.services.retry import retryable


class OpenAIClient:
    def __init__(self):
        if not settings.OPENAI_API_KEY:
            raise ValueError("OPENAI_API_KEY is required for LLM and embeddings services.")

        base_url = settings.OPENAI_BASE_URL.rstrip("/")
        # Use a short client-side timeout to fail fast and allow higher-level fallbacks
        self.client = OpenAI(
            api_key=settings.OPENAI_API_KEY,
            base_url=base_url,
            timeout=120.0,
        )
        self.model = settings.MODEL_NAME or "gpt-4o-mini"
        # self.embedding_model = settings.EMBEDDING_MODEL_NAME or "text-embedding-3-small"

    def chat(self, messages: List[Dict[str, str]], temperature: float = 0.0, max_tokens: int = 300) -> str:
        try:
            # response = retryable(
            #     self.client.chat.completions.create,
            #     model=self.model,
            #     messages=messages,
            #     temperature=temperature,
            #     max_tokens=max_tokens,
            #     timeout=20.0,
            # )
            response = self.client.chat.completions.create(
                model=self.model,
                messages=messages,
                temperature=temperature,
                max_tokens=max_tokens,
                timeout=120.0,
            )
        except Exception as e:
            print("OpenAIClient_2.chat error:", type(e).__name__, str(e))
            msg = str(e).lower()
            if "timed out" in msg or "timeout" in msg or isinstance(e, TimeoutError):
                raise TimeoutError("LLM request timed out") from e
            raise

        return response.choices[0].message.content.strip()

    # def embed(self, text: str) -> List[float]:
    #     response = self.client.embeddings.create(
    #         model=self.embedding_model,
    #         input=text
    #     )
    #     return response.data[0].embedding

# class OpenAIClient_2:
#     def __init__(self):
#         # Prefer a dedicated second API key but fall back to the primary key if not provided
#         api_key = getattr(settings, "OPENAI_API_KEY_2", None) or settings.OPENAI_API_KEY
#         if not api_key:
#             raise ValueError("An OpenAI API key (primary or secondary) is required.")

#         base_url = settings.OPENAI_BASE_URL.rstrip("/")
#         self.client = OpenAI(
#             api_key=api_key,
#             base_url=base_url,
#             timeout=120.0,
#         )
#         self.model = settings.MODEL_NAME or "gpt-4o-mini"
#         # self.embedding_model = settings.EMBEDDING_MODEL_NAME or "text-embedding-3-small"

#     def chat(self, messages: List[Dict[str, str]], temperature: float = 0.0, max_tokens: int = 300) -> str:
#         try:
#             response = self.client.chat.completions.create(
#                 model=self.model,
#                 messages=messages,
#                 temperature=temperature,
#                 max_tokens=max_tokens,   
#                                           timeout=120.0,
#                 )
            
#         except Exception as e:
#             msg = str(e).lower()
#             if "timed out" in msg or "timeout" in msg or isinstance(e, TimeoutError):
#                 raise TimeoutError("LLM request timed out") from e
#             raise

#         return response.choices[0].message.content.strip()
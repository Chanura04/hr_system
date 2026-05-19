from langchain_openai import ChatOpenAI

from app.config import settings


class LLMService:

    def __init__(self):
        self.llm = ChatOpenAI(
            api_key=settings.OPENAI_API_KEY,
            model=settings.MODEL_NAME,
            temperature=0
        )

    def invoke(self, prompt: str):
        response = self.llm.invoke(prompt)
        return response.content
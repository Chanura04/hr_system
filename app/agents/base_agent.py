from abc import ABC, abstractmethod


class BaseAgent(ABC):

    @abstractmethod
    def handle(self, query: str, context: dict) -> str:
        pass
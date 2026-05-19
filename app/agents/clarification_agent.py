from app.agents.base_agent import BaseAgent


class ClarificationAgent(BaseAgent):

    def handle(self, query: str, context: dict) -> str:
        return (
            "Clarification Agent: I need more details to process "
            "your request. Could you clarify your intent?"
        )
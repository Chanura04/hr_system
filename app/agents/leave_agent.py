from app.agents.base_agent import BaseAgent


class LeaveAgent(BaseAgent):

    def handle(self, query: str, context: dict) -> str:
        return (
            "Leave Agent: Your leave request has been submitted "
            "for manager approval."
        )
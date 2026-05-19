from app.agents.base_agent import BaseAgent


class ComplianceAgent(BaseAgent):

    def handle(self, query: str, context: dict) -> str:
        return (
            "Compliance Agent: According to company policy, "
            "all employees must complete compliance training annually."
        )
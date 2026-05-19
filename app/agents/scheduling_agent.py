from app.agents.base_agent import BaseAgent


class SchedulingAgent(BaseAgent):

    def handle(self, query: str, context: dict) -> str:
        return (
            "Scheduling Agent: Meeting has been tentatively scheduled "
            "for tomorrow at 10:00 AM."
        )
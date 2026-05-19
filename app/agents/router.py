from app.agents.scheduling_agent import SchedulingAgent
from app.agents.leave_agent import LeaveAgent
from app.agents.compliance_agent import ComplianceAgent
from app.agents.clarification_agent import ClarificationAgent


class AgentRouter:

    def __init__(self):
        self.agents = {
            "scheduling": SchedulingAgent(),
            "leave": LeaveAgent(),
            "compliance": ComplianceAgent(),
            "clarification": ClarificationAgent()
        }

    def get_agent(self, intent: str):
        return self.agents.get(intent, ClarificationAgent())
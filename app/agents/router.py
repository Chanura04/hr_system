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

        '''
            if the intent is not recognized, we can return a clarification agent that will ask the
            user for more details. This way we can handle out-of-scope queries gracefully and also have 
            a chance to route them correctly if the user provides more information.
        '''

        return self.agents.get(intent, ClarificationAgent())
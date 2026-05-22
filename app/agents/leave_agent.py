from app.agents.base_agent import BaseAgent
# from app.services.openai_client import OpenAIClient_2


class LeaveAgent(BaseAgent):
    # _SYSTEM = (
    #     "You are an HR Leave Management Assistant. Help employees understand their "
    #     "leave entitlements, submit leave requests, and check approval status. "
    #     "Be empathetic and clear about policies."
    # )

    # def __init__(self):
    #     self.llm = OpenAIClient_2()

    def handle(self, query: str, context: dict) -> str:
      
        return (
                "Leave Agent: Your leave request has been submitted for manager approval. "
            )
        
    # def handle(self, query: str, context: dict) -> str:
    #     user_msg = f"Context: {context}\n\nUser Query: {query}"
    #     try:
    #         response = self.llm.chat([
    #             {"role": "system", "content": self._SYSTEM},
    #             {"role": "user", "content": user_msg}
    #         ], max_tokens=200)
    #         return response
    #     except TimeoutError:
    #         return (
    #             "Your leave request is being processed. "
    #             "If you need immediate assistance, please contact HR directly."
    #         )
    #     except Exception:
    #         return (
    #             "Leave Agent: Your leave request has been submitted for manager approval. "
    #             "(Note: Could not reach LLM for dynamic guidance.)"
    #         )
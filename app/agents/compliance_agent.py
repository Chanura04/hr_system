from app.agents.base_agent import BaseAgent
# from app.services.openai_client import OpenAIClient_2


class ComplianceAgent(BaseAgent):
    # _SYSTEM = (
    #     "You are an HR Compliance Advisor. Provide accurate, professional answers "
    #     "about HR policies, legal requirements, and workplace regulations. "
    #     "Always recommend consulting the official HR Policy Handbook or Legal team "
    #     "for binding decisions. Do not give legal advice."
    # )

    # def __init__(self):
    #     self.llm = OpenAIClient_2()

    def handle(self, query: str, context: dict) -> str:
        
          return (
                "Compliance Agent: According to company policy, you request is processing. Please contact HR directly for urgent matters. "
               
            )
        

    #  def handle(self, query: str, context: dict) -> str:
    #     user_msg = f"Context: {context}\n\nUser Query: {query}"
    #     try:
    #         response = self.llm.chat([
    #             {"role": "system", "content": self._SYSTEM},
    #             {"role": "user", "content": user_msg}
    #         ], max_tokens=200)
    #         return response
    #     except TimeoutError:
    #         return (
    #             "Your compliance inquiry has been received. "
    #             "Please contact HR directly for urgent matters."
    #         )
    #     except Exception:
    #         return (
    #             "Compliance Agent: According to company policy, "
    #             "all employees must complete compliance training annually. "
    #             "(Note: Could not reach LLM for dynamic guidance.)"
    #         )
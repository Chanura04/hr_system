from app.agents.base_agent import BaseAgent
# from app.services.openai_client import OpenAIClient_2


class ClarificationAgent(BaseAgent):
    # _SYSTEM = (
    #     "You are an HR Assistant handling an unclear request. "
    #     "Ask ONE clear, specific follow-up question to understand what the employee needs. "
    #     "Be polite, brief, and suggest the most likely intent to help them. "
    #     "Possible topics: scheduling, leave, or compliance/policy questions."
    # )

    # def __init__(self):
    #     self.llm = OpenAIClient_2()

    def handle(self, query: str, context: dict) -> str:
        
        return (
                "Clarification Agent: I need more details to process "
                "your request. Could you clarify your intent?"
            )
        
    # def handle(self, query: str, context: dict) -> str:
    #     user_msg = f"Context: {context}\n\nUser Query: {query}"
    #     try:
    #         response = self.llm.chat([
    #             {"role": "system", "content": self._SYSTEM},
    #             {"role": "user", "content": user_msg}
    #         ], max_tokens=150)
    #         return response
    #     except TimeoutError:
    #         return (
    #             "I need more details to process your request. "
    #             "Could you please rephrase or provide more information?"
    #         )
    #     except Exception:
    #         return (
    #             "Clarification Agent: I need more details to process "
    #             "your request. Could you clarify your intent?"
    #         )
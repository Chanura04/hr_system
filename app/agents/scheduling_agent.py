from app.agents.base_agent import BaseAgent
# from app.services.openai_client import OpenAIClient_2


class SchedulingAgent(BaseAgent):
    # _SYSTEM = (
    #     "You are an HR Scheduling Assistant. Help employees with meeting bookings, "
    #     "calendar management, and shift planning. Be concise, friendly, and practical. "
    #     "Use the available slots and employee info provided to give specific answers."
    # )

    # def __init__(self):
    #     self.llm = OpenAIClient_2()

    def handle(self, query: str, context: dict) -> str:
        
        return (
                "Scheduling Agent: Meeting has been tentatively scheduled. "
                
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
    #             "Your scheduling request is being processed. "
    #             "Please check your calendar or contact the scheduler for details."
    #         )
    #     except Exception:
    #         return (
    #             "Scheduling Agent: Meeting has been tentatively scheduled. "
    #             "(Note: Could not reach LLM for dynamic guidance.)"
    #         )
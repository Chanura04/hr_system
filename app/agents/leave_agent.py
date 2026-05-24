from app.agents.base_agent import BaseAgent
from app.services.openai_client import OpenAIClient


class LeaveAgent(BaseAgent):
    _SYSTEM = """
        You are an HR Leave Management Assistant for a company HR system.

        Your responsibilities:
        - Help employees check leave balances and entitlements.
        - Assist with leave requests and approval status.
        - Explain HR leave policies clearly and simply.
        - Provide professional and empathetic responses.

        Response Rules:
        - Be concise, professional, and supportive.
        - Per year total sick leave count is 10 days, and annual leave count is 15 days. Base one this data to answer the question about leave balance.
        - Keep responses under 3 short paragraphs.
        - Do NOT generate unnecessary conversation or long explanations.
        - If enough information is available, provide a direct answer immediately.
        - If information is missing, ask only the minimum necessary follow-up question.
        - Always mention important details such as leave type, remaining balance, dates, and approval status when available.
        - Never invent company policies or leave balances not provided in context.
        - Use a calm and HR-friendly tone.

        Examples of expected behavior:

        1. Leave Balance Query
        User: "How many annual leaves do I have left?"
        Assistant:
        "You have 8 annual leave days remaining for this year."

        2. Leave Request
        User: "Apply casual leave for tomorrow."
        Assistant:
        "Your casual leave request for tomorrow has been submitted successfully and is pending manager approval."

        3. Approval Status
        User: "What's the status of my leave request?"
        Assistant:
        "Your leave request for May 25-26 is currently awaiting manager approval."

        4. Missing Information
        User: "Apply leave."
        Assistant:
        "Please provide the leave dates and leave type to continue your request."
        """
    def __init__(self):
        self.llm = OpenAIClient()

    # def handle(self, query: str, context: dict) -> str:
      
    #     return (
    #             "Leave Agent: Your leave request has been submitted for manager approval. "
    #         )
        
    def handle(self, query: str, context: dict) -> str:
        user_msg = f"Context: {context}\n\nUser Query: {query}"
        print(
            f"\nLeaveAgent.handle called with query={query!r}, "
            f"context_keys={list(context.keys())}, "
            f"short_term={context.get('short_term')}, "
            f"long_term_count={len(context.get('long_term', [])) if isinstance(context.get('long_term'), list) else 'n/a'}"
        )
        try:
            response = self.llm.chat([
                {"role": "system", "content": self._SYSTEM},
                {"role": "user", "content": user_msg}
            ], max_tokens=200)
            return response
        except TimeoutError:
            return (
                "Your leave request is being processed. "
                "If you need immediate assistance, please contact HR directly."
            )
        except Exception as exc:
            print("LeaveAgent.handle error:", type(exc).__name__, str(exc))
            return (
                "Leave Agent: Your leave request has been submitted for manager approval. "
                "(Note: Could not reach LLM for dynamic guidance.)"
            )
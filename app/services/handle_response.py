
from typing import Tuple, TypedDict


class AgentResponseHandler:

    def build_prompt(self, query: str, history: str) -> str:

        return (
            "Based on the following conversation history and the new user query, generate a helpful and concise response.\n\n"
            "Conversation History:\n"
            f"History: {history}\n\n"
            f"User Query: {query}"
        
        )
    
    def _llm_classification(self, text: str) -> Tuple[str, float]:
        prompt = self._build_prompt(text)
        try:
            raw_response = self.llm.chat([
                {"role": "system", "content": "You are an HR assistant."},
                {"role": "user", "content": prompt}
            ], temperature=0.0)
        except Exception:
            return TimeoutError("LLM request failed")
           
import json
import re
from typing import Dict, List, Tuple

from app.services.embedding_service import EmbeddingService
from app.services.openai_client import OpenAIClient


INTENT_DEFINITIONS: Dict[str, str] = {
    "scheduling": (
        "Requests about booking, rescheduling, cancelling, or confirming meetings, interviews, "
        "and calendar events."
    ),
    "leave": (
        "Requests about vacation, sick leave, time off requests, and absence approvals."
    ),
    "compliance": (
        "Requests about company policy, training requirements, regulatory compliance, "
        "and HR rules."
    ),
    "clarification": (
        "Requests that are unclear, out of scope for scheduling, leave, or compliance, "
        "or that need more information before routing."
    )
}


class IntentClassifier:

    def __init__(self):
        self.llm = OpenAIClient()
        self.embedding_service = EmbeddingService()
        self.intent_embeddings: Dict[str, List[float]] = {}

    def _ensure_intent_embeddings(self) -> None:
        if self.intent_embeddings:
            return

        for intent, description in INTENT_DEFINITIONS.items():
            self.intent_embeddings[intent] = self.embedding_service.embed(description)

    def classify(self, text: str) -> Tuple[str, float]:
        clean_text = text.strip()
        llm_intent, llm_confidence = self._llm_classification(clean_text)
        semantic_intent, semantic_similarity = self._semantic_match(clean_text)

        # Relax threshold if LLM is highly confident or keywords are present
        if semantic_similarity < 0.35 and llm_confidence < 0.8:
            return "clarification", 0.40

        intent = self._select_intent(llm_intent, semantic_intent, semantic_similarity)
        confidence = self._calibrate_confidence(llm_confidence, semantic_similarity, intent)

        return intent, confidence

    def _llm_classification(self, text: str) -> Tuple[str, float]:
        prompt = self._build_prompt(text)
        try:
            raw_response = self.llm.chat([
                {"role": "system", "content": "You are an HR request classifier."},
                {"role": "user", "content": prompt}
            ], temperature=0.0)
        except Exception:
            return self._keyword_fallback(text)

        parsed = self._parse_response(raw_response)
        if parsed:
            return parsed["intent"], parsed["confidence"]

        return self._keyword_fallback(text)

    def _build_prompt(self, text: str) -> str:
        intent_lines = "\n".join(
            f"- {intent}: {description}"
            for intent, description in INTENT_DEFINITIONS.items()
        )

        return (
            "Classify the user request into one of the following intents. "
            "Respond with JSON only, using keys \"intent\" and \"confidence\". "
            "Confidence should be a number between 0.0 and 1.0.\n\n"
            f"Available intents:\n{intent_lines}\n\n"
            f"User request: \"{text}\""
        )

    def _parse_response(self, content: str) -> Dict[str, float]:
        try:
            payload = json.loads(content)
            intent = payload.get("intent", "clarification")
            confidence = float(payload.get("confidence", 0.0))
            return {"intent": intent, "confidence": max(0.0, min(confidence, 1.0))}
        except (ValueError, json.JSONDecodeError):
            match = re.search(r"\{.*\}", content, re.S)
            if match:
                try:
                    payload = json.loads(match.group())
                    intent = payload.get("intent", "clarification")
                    confidence = float(payload.get("confidence", 0.0))
                    return {"intent": intent, "confidence": max(0.0, min(confidence, 1.0))}
                except (ValueError, json.JSONDecodeError):
                    pass

        return {}

    def _semantic_match(self, text: str) -> Tuple[str, float]:
        self._ensure_intent_embeddings()
        request_embedding = self.embedding_service.embed(text)
        best_intent = "clarification"
        best_score = 0.0

        for intent, intent_embedding in self.intent_embeddings.items():
            score = self.embedding_service.cosine_similarity(request_embedding, intent_embedding)
            if score > best_score:
                best_score = score
                best_intent = intent

        return best_intent, round(best_score, 2)

    def _select_intent(
        self,
        llm_intent: str,
        semantic_intent: str,
        semantic_similarity: float
    ) -> str:
        if semantic_intent != llm_intent and semantic_similarity >= 0.7:
            return semantic_intent

        return llm_intent if llm_intent in INTENT_DEFINITIONS else semantic_intent

    def _calibrate_confidence(
        self,
        llm_confidence: float,
        semantic_similarity: float,
        intent: str
    ) -> float:
        base_confidence = (llm_confidence * 0.6) + (semantic_similarity * 0.4)
        if intent == "clarification":
            return round(max(0.35, min(base_confidence, 0.55)), 2)

        return round(max(0.5, min(base_confidence, 0.98)), 2)

    def _keyword_fallback(self, text: str) -> Tuple[str, float]:
        lower = text.lower()
        if "meeting" in lower or "schedule" in lower:
            return "scheduling", 0.60
        if "leave" in lower or "vacation" in lower or "absent" in lower:
            return "leave", 0.60
        if "policy" in lower or "compliance" in lower or "training" in lower:
            return "compliance", 0.60

        return "clarification", 0.40
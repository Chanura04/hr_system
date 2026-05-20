import json
import re
from typing import Dict, List, Tuple

import numpy as np
from sentence_transformers import SentenceTransformer

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
        self.semantic_model = SentenceTransformer("all-MiniLM-L6-v2")
        self.intent_embeddings: Dict[str, np.ndarray] = {}
        

    def _ensure_intent_embeddings(self) -> None:
        if self.intent_embeddings:
            return

        for intent, description in INTENT_DEFINITIONS.items():
            embedding = self.semantic_model.encode(
                description,
                convert_to_numpy=True,
                normalize_embeddings=True
            )
            self.intent_embeddings[intent] = embedding

    def classify(self, text: str) -> Tuple[str, float]:
        clean_text = text.strip()
        llm_intent, llm_confidence = self._llm_classification(clean_text)
        semantic_intent, semantic_similarity = self._semantic_match(clean_text)

        # print(f"LLM intent: {llm_intent} (confidence: {llm_confidence}), "
        #       f"Semantic intent: {semantic_intent} (similarity: {semantic_similarity})")

        #if LLM conidence is enough and it intent is valid, use it. Otherwise, fallback to semantic intent
        if llm_intent in INTENT_DEFINITIONS and llm_confidence >= 0.35:
            intent = llm_intent
        else:
            intent = semantic_intent

        # Handle the LLm 'Hallucination' case - when LLM confidence is low but it predicts a valid intent, we can check semantic similarity to validate it
        if llm_intent in INTENT_DEFINITIONS and llm_confidence < 0.4 and semantic_similarity >= 0.7:
            intent = semantic_intent

        confidence = self.calibrate_confidence(llm_confidence, semantic_similarity, intent)

        return intent, confidence

    def _llm_classification(self, text: str) -> Tuple[str, float]:
        prompt = self._build_prompt(text)
        try:
            raw_response = self.llm.chat([
                {"role": "system", "content": "You are an HR request classifier."},
                {"role": "user", "content": prompt}
            ], temperature=0.0)
        except Exception:
            return self._semantic_fallback(text)

        parsed = self._parse_response(raw_response)
        if parsed:
            return parsed["intent"], parsed["confidence"]

        return self._semantic_fallback(text)

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
        request_embedding = self.semantic_model.encode(
            text,
            convert_to_numpy=True,
            normalize_embeddings=True
        )

        best_intent = "clarification"
        best_score = 0.0
        for intent, intent_embedding in self.intent_embeddings.items():
            score = float(np.dot(request_embedding, intent_embedding))
            if score > best_score:
                best_score = score
                best_intent = intent

        return best_intent, round(best_score, 2)

    def calibrate_confidence(
        self,
        llm_confidence: float,
        semantic_similarity: float,
        intent: str
    ) -> float:
        base_confidence = (llm_confidence * 0.6) + (semantic_similarity * 0.4)
        if intent == "clarification":
            return round(max(0.35, min(base_confidence, 0.55)), 2)

        return round(max(0.5, min(base_confidence, 0.98)), 2)

    '''
    Backup fallback when LLM fails to respond or parse - we can still provide a guess based on semantic similarity
    '''
    def _semantic_fallback(self, text: str) -> Tuple[str, float]:
        intent, similarity = self._semantic_match(text)
        if intent == "clarification":
            return "clarification", 0.40

        calibrated = max(0.35, min(similarity + 0.2, 0.75))
        return intent, round(calibrated, 2)
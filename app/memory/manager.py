from sqlalchemy.orm import Session

from app.memory.stm import ShortTermMemory
from app.memory.ltm import LongTermMemory
from app.memory.scorer import SignificanceScorer
from app.agents.classifier import IntentClassifier

class MemoryManager:

    def __init__(self):
        self.stm = ShortTermMemory()
        self.classifier = IntentClassifier()

    def store(self, db: Session, user_id: str, message: str, intent: str, confidence: float):
        self.stm.add(user_id, message)

        confidence_result = confidence
        intent_result = intent
        print(f"Intent: {intent_result}, confidence: {confidence_result}")

        if confidence_result >= 0.6:
            LongTermMemory.add(
                db,
                user_id,
                message,
                confidence_result
            )

    def retrieve_context(self, db: Session, user_id: str):
        stm_context = self.stm.get(user_id)
        ltm_context = LongTermMemory.retrieve(db, user_id)

        return {
            "short_term": stm_context,
            "long_term": [x.content for x in ltm_context]
        }
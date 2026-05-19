from sqlalchemy.orm import Session

from app.memory.stm import ShortTermMemory
from app.memory.ltm import LongTermMemory
from app.memory.scorer import SignificanceScorer


class MemoryManager:

    def __init__(self):
        self.stm = ShortTermMemory()

    def store(self, db: Session, user_id: str, message: str):
        self.stm.add(user_id, message)

        significance = SignificanceScorer.score(message)

        if significance >= 0.5:
            LongTermMemory.add(
                db,
                user_id,
                message,
                significance
            )

    def retrieve_context(self, db: Session, user_id: str):
        stm_context = self.stm.get(user_id)
        ltm_context = LongTermMemory.retrieve(db, user_id)

        return {
            "short_term": stm_context,
            "long_term": [x.content for x in ltm_context]
        }
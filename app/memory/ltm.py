from datetime import datetime

from sqlalchemy import Column, Integer, String, Float, DateTime
from sqlalchemy.orm import Session

from zoneinfo import ZoneInfo

from app.database import Base


class LongTermMemoryRecord(Base):
    __tablename__ = "long_term_memory"

    id = Column(Integer, primary_key=True)
    user_id = Column(String)
    content = Column(String)
    significance = Column(Float)
    
    created_at = Column(
        DateTime(timezone=True),
        default=lambda: datetime.now(ZoneInfo("Asia/Colombo"))
    )



class LongTermMemory:

    @staticmethod
    def add(
        db: Session,
        user_id: str,
        content: str,
        significance: float
    ):

        record = LongTermMemoryRecord(
            user_id=user_id,
            content=content,
            significance=significance
        )

        db.add(record)
        db.commit()

    @staticmethod
    def retrieve(db: Session, user_id: str):
        return db.query(LongTermMemoryRecord).filter(
            LongTermMemoryRecord.user_id == user_id
        ).order_by(LongTermMemoryRecord.created_at.desc()).all()
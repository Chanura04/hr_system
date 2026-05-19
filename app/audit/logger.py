import uuid

from sqlalchemy.orm import Session

from app.audit.models import AuditLog


class AuditLogger:

    @staticmethod
    def append_log(
        db: Session,
        user_id: str,
        intent: str,
        confidence: float,
        agent: str,
        status: str
    ) -> str:

        request_id = str(uuid.uuid4())

        record = AuditLog(
            request_id=request_id,
            user_id=user_id,
            intent=intent,
            confidence=confidence,
            agent=agent,
            status=status
        )

        db.add(record)
        db.commit()

        return request_id
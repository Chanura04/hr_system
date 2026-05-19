from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import HTMLResponse
from sqlalchemy.orm import Session

from app.database import get_db
from app.schemas import AgentResponse, RequestPayload
from app.agents.orchestrator import Orchestrator
from app.audit.models import AuditLog
from app.memory.ltm import LongTermMemoryRecord


router = APIRouter()

orchestrator = Orchestrator()


@router.post("/request", response_model=AgentResponse)
def process_request(payload: RequestPayload, db: Session = Depends(get_db)):
    try:
        return orchestrator.process(
            db,
            payload.user_id,
            payload.message
        )
    except Exception:
        raise HTTPException(
            status_code=500,
            detail="Unable to process request right now. Please try again later."
        )


@router.get("/audit")
def get_audits(db: Session = Depends(get_db)):
    logs = db.query(AuditLog).order_by(AuditLog.created_at.desc()).all()
    return [
        {
            "request_id": log.request_id,
            "user_id": log.user_id,
            "intent": log.intent,
            "confidence": log.confidence,
            "agent": log.agent,
            "status": log.status,
            "created_at": log.created_at.isoformat() if log.created_at else None,
        }
        for log in logs
    ]


@router.get("/memory/{user_id}")
def get_memory(user_id: str, db: Session = Depends(get_db)):
    # Retrieve STM from the volatile storage
    stm_content = orchestrator.memory_manager.stm.get(user_id)
    
    records = db.query(LongTermMemoryRecord).filter(
        LongTermMemoryRecord.user_id == user_id
    ).order_by(LongTermMemoryRecord.created_at.desc()).all()

    return {
        "user_id": user_id,
        "short_term_memory": stm_content,
        "long_term_memory": [
            {
                "content": record.content,
                "significance": record.significance,
                "created_at": record.created_at.isoformat() if record.created_at else None,
            }
            for record in records
        ]
    }


@router.delete("/memory/{user_id}")
def clear_memory(user_id: str, db: Session = Depends(get_db)):
    records = db.query(LongTermMemoryRecord).filter(
        LongTermMemoryRecord.user_id == user_id
    )

    deleted = records.delete()
    db.commit()

    return {
        "deleted": deleted
    }
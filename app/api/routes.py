

from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import HTMLResponse
from sqlalchemy.orm import Session

from app.database import get_db
from app.schemas import AgentResponse, RequestPayload
from app.agents.orchestrator import Orchestrator
from app.audit.models import AuditLog
from app.memory.ltm import LongTermMemoryRecord

"""
This  defines the RESTful endpoints for the application, acting as the interface between 
the HTTP layer and the core logic. 
"""

router = APIRouter()

orchestrator = Orchestrator()

"""Request Routing: Passing user messages to the Orchestrator for processing."""
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


"""Audit Observability: Providing read access to the transaction logs."""
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

"""Memory Inspection: Endpoints to view and manage user-specific short-term and long-term memory."""
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

    # Also clear volatile Short-Term Memory
    if user_id in orchestrator.memory_manager.stm.memory:
        del orchestrator.memory_manager.stm.memory[user_id]

    deleted = records.delete()
    db.commit()

    return {
        "deleted": deleted
    }
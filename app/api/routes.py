

import uuid
from threading import Lock
from typing import Dict

from fastapi import APIRouter, Depends, HTTPException, BackgroundTasks
from fastapi.responses import HTMLResponse
from sqlalchemy.orm import Session

from app.database import SessionLocal, get_db
from app.schemas import (
    AgentResponse,
    BackgroundJobResponse,
    BackgroundRequestStatus,
    RequestPayload,
)
from app.agents.orchestrator import Orchestrator
from app.audit.models import AuditLog
from app.memory.ltm import LongTermMemoryRecord

"""
This  defines the RESTful endpoints for the application, acting as the interface between 
the HTTP layer and the core logic. 
"""

router = APIRouter()

orchestrator = Orchestrator()
background_jobs: Dict[str, dict] = {}
background_jobs_lock = Lock()


def _get_background_job(job_id: str) -> dict | None:
    with background_jobs_lock:
        return background_jobs.get(job_id)


def _set_background_job(job_id: str, payload: dict) -> None:
    with background_jobs_lock:
        background_jobs[job_id] = payload


def _update_background_job(job_id: str, updates: dict) -> None:
    with background_jobs_lock:
        if job_id in background_jobs:
            background_jobs[job_id].update(updates)


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


def _process_background_request(job_id: str, user_id: str, message: str) -> None:
    db = SessionLocal()
    try:
        _update_background_job(job_id, {"status": "processing"})
        result = orchestrator.process(db, user_id, message)
        _update_background_job(job_id, {"status": "completed", "result": result})
    except Exception as exc:
        _update_background_job(job_id, {"status": "failed", "error": str(exc)})
    finally:
        db.close()


@router.post("/request/background", response_model=BackgroundJobResponse)
def submit_background_request(
    payload: RequestPayload,
    background_tasks: BackgroundTasks
):
    job_id = str(uuid.uuid4())
    _set_background_job(job_id, {
        "job_id": job_id,
        "status": "pending",
        "result": None,
        "error": None,
    })
    background_tasks.add_task(
        _process_background_request,
        job_id,
        payload.user_id,
        payload.message,
    )

    return {"job_id": job_id, "status": "pending"}


@router.get("/request/status/{job_id}", response_model=BackgroundRequestStatus)
def get_background_request_status(job_id: str):
    job = _get_background_job(job_id)
    if job is None:
        raise HTTPException(status_code=404, detail="Background request not found.")

    return {
        "job_id": job_id,
        "status": job["status"],
        "result": job.get("result"),
        "error": job.get("error"),
    }


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
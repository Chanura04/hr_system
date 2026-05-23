from typing import Optional, List
from pydantic import BaseModel


class RequestPayload(BaseModel):
    user_id: str
    message: str


class AgentResponse(BaseModel):
    request_id: str
    intent: str
    confidence: float
    response: str
    agent_used: str
    context_used: Optional[dict]


class BackgroundJobResponse(BaseModel):
    job_id: str
    status: str


class BackgroundRequestStatus(BaseModel):
    job_id: str
    status: str
    result: Optional[AgentResponse] = None
    error: Optional[str] = None


class AuditRecord(BaseModel):
    request_id: str
    user_id: str
    intent: str
    confidence: float
    agent: str
    status: str
    created_at: Optional[str]

    class Config:
        from_attributes = True


class MemoryRecord(BaseModel):
    user_id: str
    content: str
    significance: float
    created_at: Optional[str]

    class Config:
        from_attributes = True
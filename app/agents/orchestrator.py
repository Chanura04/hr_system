from sqlalchemy.orm import Session

from app.memory.manager import MemoryManager
from app.audit.logger import AuditLogger
from app.services.langgraph_flow import build_graph


class Orchestrator:

    def __init__(self):
        self.graph = build_graph()
        self.memory_manager = MemoryManager()

    def process(
        self,
        db: Session,
        user_id: str,
        message: str
    ):

        context = self.memory_manager.retrieve_context(db, user_id)

        initial_state = {
            "query": message,
            "intent": "",
            "confidence": 0.0,
            "response": "",
            "context": context
        }

        try:
            result = self.graph.invoke(initial_state)
            self.memory_manager.store(db, user_id, message)

            request_id = AuditLogger.append_log(
                db=db,
                user_id=user_id,
                intent=result["intent"],
                confidence=result["confidence"],
                agent=result["intent"],
                status="success"
            )

            return {
                "request_id": request_id,
                "intent": result["intent"],
                "confidence": result["confidence"],
                "response": result["response"],
                "agent_used": result["intent"],
                "context_used": context
            }

        except Exception:
            request_id = AuditLogger.append_log(
                db=db,
                user_id=user_id,
                intent="clarification",
                confidence=0.0,
                agent="clarification",
                status="failed"
            )

            return {
                "request_id": request_id,
                "intent": "clarification",
                "confidence": 0.0,
                "response": "Unable to process your request at this time. Please try again in a few minutes.",
                "agent_used": "clarification",
                "context_used": context
            }
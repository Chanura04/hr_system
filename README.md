# HR Multi-Agent Automation Platform

This project is a Python-based HR assistant engine built with FastAPI, Langgraph, SQLite, and LLM-based intent classification.

## Architecture

- `app/main.py` - FastAPI application setup with global error handling.
- `app/api/routes.py` - REST endpoints for request handling, audit retrieval, memory management, and health checks.
- `app/agents/orchestrator.py` - Central orchestrator that routes user requests through the Langgraph workflow.
- `app/services/langgraph_flow.py` - Langgraph graph with intent classification and agent routing.
- `app/agents/classifier.py` - LLM-backed classification with embeddings, semantic similarity, and confidence calibration.
- `app/agents/router.py` - Maps inferred intents to specialist agents.
- `app/memory/` - Two-tier memory with STM and LTM and significance scoring.
- `app/audit/` - Append-only audit logger and storage.
- `app/services/openai_client.py` - OpenAI SDK client for chat completions and embeddings using configured base URL.
- `app/services/embedding_service.py` - Semantic similarity utilities.
- `flask_app.py` - Simple Flask UI for submitting requests, viewing audit logs, and checking user memory.
- `streamlit_app.py` - Optional Streamlit UI for browser interaction with the FastAPI backend.

## API Endpoints

- `POST /request` - Process a user request and return intent, confidence, response, and routed agent.
- `GET /audit` - Retrieve audit log entries.
- `GET /memory/{user_id}` - Retrieve stored long-term memory for a user.
- `DELETE /memory/{user_id}` - Clear long-term memory for a user.
- `GET /health` - Health check endpoint.

## Deployment

1. Copy or update `.env` with `OPENAI_API_KEY`, `OPENAI_BASE_URL`, `MODEL_NAME`, `EMBEDDING_MODEL_NAME`, and `SQLITE_DB`.
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Start the FastAPI service:
   ```bash
   python run.py
   ```
4. Start the Flask UI in a separate terminal:
   ```bash
   python flask_app.py
   ```

Optional: Start the Streamlit UI instead with:
   ```bash
   streamlit run streamlit_app.py
   ```

## Notes

- The intent classifier now uses an LLM plus embeddings for robust intent routing.
- Low-confidence or out-of-scope requests are routed to the `ClarificationAgent`.
- Raw Python stack traces are hidden from API clients via a global exception handler.
- Audit logs are append-only, and memory reads are exposed through safe endpoints.

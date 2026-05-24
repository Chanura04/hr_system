from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import JSONResponse, HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from app.config import settings
from app.database import Base, engine
from app.api.routes import router
from app.api.health import health_router


Base.metadata.create_all(bind=engine)

app = FastAPI(title=settings.APP_NAME)

# Mount static files and templates so FastAPI can serve the frontend
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")


@app.get("/", response_class=HTMLResponse)
async def index(request: Request):
    return templates.TemplateResponse(
        request,
        "index.html",
        {
            "user_id": "user-123",
            "message": "Please schedule a meeting with my manager.",
        },
    )

"""
Global Exception Handling: A catch-all handler to ensure that unexpected errors are 
logged and a generic error message is returned to the client, preventing exposure of internal server details.
"""
@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    if isinstance(exc, HTTPException):
        return JSONResponse(
            status_code=exc.status_code,
            content={"detail": exc.detail}
        )

    return JSONResponse(
        status_code=500,
        content={
            "status": "error",
            "message": "Internal server error. Please try again later."
        }
    )

app.include_router(router)
app.include_router(health_router)
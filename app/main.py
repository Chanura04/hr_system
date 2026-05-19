from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import JSONResponse

from app.config import settings
from app.database import Base, engine
from app.api.routes import router
from app.api.health import health_router


Base.metadata.create_all(bind=engine)

app = FastAPI(title=settings.APP_NAME)


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
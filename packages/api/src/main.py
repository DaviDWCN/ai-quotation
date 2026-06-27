from fastapi import FastAPI
from pydantic import BaseModel
from src.config import settings
from src.routers import drafts

app = FastAPI(title=settings.app_name)

app.include_router(drafts.router)

class HealthResponse(BaseModel):
    status: str

@app.get("/healthz", response_model=HealthResponse)
def health_check() -> HealthResponse:
    return HealthResponse(status="ok")

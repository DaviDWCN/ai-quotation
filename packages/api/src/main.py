from fastapi import FastAPI
from pydantic import BaseModel
from src.config import settings
from src.routers.drafts import router as drafts_router

app = FastAPI(title=settings.app_name)

app.include_router(drafts_router, prefix="/api")

class HealthResponse(BaseModel):
    status: str

@app.get("/healthz", response_model=HealthResponse)
def health_check() -> HealthResponse:
    return HealthResponse(status="ok")

from fastapi import FastAPI
from pydantic import BaseModel
from src.config import settings

app = FastAPI(title=settings.app_name)

class HealthResponse(BaseModel):
    status: str

@app.get("/healthz", response_model=HealthResponse)
def health_check() -> HealthResponse:
    return HealthResponse(status="ok")

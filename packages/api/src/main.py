from fastapi import FastAPI
from pydantic import BaseModel
from src.config import settings
from src.routers import wecom_callback
from src.routers.drafts import router as drafts_router

app = FastAPI(title=settings.app_name)

app.include_router(wecom_callback.router, prefix="/api/wecom", tags=["wecom"])
app.include_router(drafts_router, prefix="/api")

class HealthResponse(BaseModel):
    status: str

@app.get("/healthz", response_model=HealthResponse)
async def healthz():
    return HealthResponse(status="ok")

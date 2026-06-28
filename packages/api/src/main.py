from fastapi import FastAPI
from pydantic import BaseModel
from src.config import settings
from src.routers import wecom_callback
from src.routers.drafts import router as drafts_router
from src.routers.gateway import router as gateway_router

app = FastAPI(title=settings.app_name)

app.include_router(wecom_callback.router, prefix="/api/wecom", tags=["wecom"])
app.include_router(drafts_router, prefix="/api")
app.include_router(gateway_router, prefix="/api/gateway", tags=["gateway"])

class HealthResponse(BaseModel):
    status: str

@app.get("/healthz", response_model=HealthResponse)
async def healthz() -> HealthResponse:
    return HealthResponse(status="ok")

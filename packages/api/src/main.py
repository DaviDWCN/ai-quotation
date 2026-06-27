import asyncio
from contextlib import asynccontextmanager
from typing import AsyncGenerator
from fastapi import FastAPI
from pydantic import BaseModel
from src.config import settings
from src.routers import gateway
from src.services.gateway.sync_service import sync_service

@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator[None, None]:
    # Start background status sync
    sync_task = asyncio.create_task(sync_service.start_periodic_sync(interval_seconds=300))
    yield
    # Cleanup
    sync_service.stop_periodic_sync()
    await sync_task

app = FastAPI(title=settings.app_name, lifespan=lifespan)

class HealthResponse(BaseModel):
    status: str

@app.get("/healthz", response_model=HealthResponse)
def health_check() -> HealthResponse:
    return HealthResponse(status="ok")

app.include_router(gateway.router, prefix="/api")

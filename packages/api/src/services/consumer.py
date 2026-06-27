import json
import logging
import asyncio
from typing import Any, Dict
from src.services.draft.service import DraftService
from src.db.session import async_session_factory
from src.services.matching.engine import MatchingEngine
from src.services.notification.service import NotificationService
from shared.types.master_data import Customer, Material
from shared.mq.rabbitmq import RabbitMQAdapter
from src.config import settings
from pathlib import Path

logger = logging.getLogger(__name__)

def load_mock_master_data() -> tuple[list[Customer], list[Material]]:
    fixture_path = Path(__file__).parent.parent.parent / "tests" / "fixtures" / "mock_master_data.json"
    if not fixture_path.exists():
        return [], []
    with open(fixture_path, "r") as f:
        data = json.load(f)
    customers = [Customer(**c) for c in data.get("customers", [])]
    materials = [Material(**m) for m in data.get("materials", [])]
    return customers, materials

async def process_ai_result(body: bytes) -> None:
    try:
        data = json.loads(body)
        customers, materials = load_mock_master_data()
        engine = MatchingEngine(customers, materials)
        notification = NotificationService()

        async with async_session_factory() as session:
            service = DraftService(session, engine, notification)
            draft = await service.create_draft_from_ai_result(data)
            logger.info(f"Draft created: {draft.id}")
    except Exception as e:
        logger.error(f"Error processing AI result: {e}")

async def start_consumer() -> None:
    mq_url = getattr(settings, "rabbitmq_url", "amqp://guest:guest@localhost:5672/")
    adapter = RabbitMQAdapter(mq_url)

    await adapter.connect()
    logger.info("MQ Consumer connected, subscribing to quotation.parse")

    await adapter.subscribe("quotation.parse", process_ai_result)

    # Keep the consumer running
    while True:
        await asyncio.sleep(1)

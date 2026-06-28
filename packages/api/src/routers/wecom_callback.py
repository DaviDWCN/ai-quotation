import logging
from collections import deque
from typing import Dict, Union

from fastapi import APIRouter, Query, Request
from fastapi.responses import PlainTextResponse
from packages.shared.mq.rabbitmq import RabbitMQAdapter
from src.config import settings
from src.services.wecom.message import (
    WeComFileMessage,
    WeComImageMessage,
    WeComTextMessage,
)
from src.services.wecom.mock_wecom import MockWeComAdapter
from src.services.wecom.webhook import (
    handle_webhook_request,
    parse_xml_payload,
    verify_signature,
)

router = APIRouter()
logger = logging.getLogger(__name__)

# Bounded cache for idempotency to avoid memory leak
MAX_PROCESSED_MESSAGES = 1000
processed_messages: deque[str] = deque(maxlen=MAX_PROCESSED_MESSAGES)

# Initialize Adapters
wecom_adapter = MockWeComAdapter()
mq_adapter = RabbitMQAdapter(url=settings.rabbitmq_url)


@router.get("/callback", response_class=PlainTextResponse)
async def wecom_verify(
    msg_signature: str = Query(...),
    timestamp: str = Query(...),
    nonce: str = Query(...),
    echostr: str = Query(...),
) -> str:
    """Verify WeCom webhook URL."""
    result = verify_signature(msg_signature, timestamp, nonce, echostr)
    if result:
        return result
    return ""


@router.post("/callback")
async def wecom_callback(
    request: Request,
    msg_signature: str = Query(...),
    timestamp: str = Query(...),
    nonce: str = Query(...),
) -> Dict[str, str]:
    """Handle WeCom webhook callback."""
    body = await request.body()
    xml_data = body.decode("utf-8")
    payload = await parse_xml_payload(xml_data)

    # Idempotency check
    msg_id = payload.get("MsgId")
    if msg_id and msg_id in processed_messages:
        logger.info(f"Message {msg_id} already processed, skipping.")
        return {"status": "ok"}

    # Process message (includes downloading files)
    processed_data = await handle_webhook_request(payload, adapter=wecom_adapter)

    # Convert Pydantic models to dict for MQ serialization
    mq_payload = processed_data.copy()
    data = mq_payload.get("data")
    if isinstance(data, (WeComTextMessage, WeComImageMessage, WeComFileMessage)):
        mq_payload["data"] = data.model_dump()  # type: ignore[assignment]

    # Publish to MQ
    try:
        if not mq_adapter.connected:
            await mq_adapter.connect()
        await mq_adapter.publish(topic="quotation.parse", message=mq_payload)
    except Exception as e:
        logger.error(f"Failed to publish to MQ: {e}")

    if msg_id:
        processed_messages.append(msg_id)
    return {"status": "ok"}

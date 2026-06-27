from fastapi import APIRouter, Request, Query, HTTPException, Response
from typing import Optional
import logging
import xmltodict
from ..services.wecom.webhook import WebhookHandler
from ..services.wecom.message import MessageProcessor
from ..services.wecom.mock_wecom import MockWeComAdapter
from ..services.storage.mock_storage import MockStorageAdapter
from src.config import settings

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/wecom", tags=["wecom"])

# These would ideally be injected or come from a dependency
# For Task-004 we use mock adapters
wecom_adapter = MockWeComAdapter()
storage_adapter = MockStorageAdapter()

# Using a mock for MQ as well for testing
class MockMQAdapter:
    async def publish(self, topic: str, message: any) -> None:
        print(f"Mock MQ Publish to {topic}: {message}")
mq_adapter = MockMQAdapter()

webhook_handler = WebhookHandler(
    token=settings.wecom_token,
    encoding_aes_key=settings.wecom_aes_key,
    app_id=settings.wecom_app_id
)
message_processor = MessageProcessor(wecom_adapter, storage_adapter, mq_adapter) # type: ignore

@router.get("/callback")
async def verify_webhook(
    msg_signature: str,
    timestamp: str,
    nonce: str,
    echostr: str
):
    """
    AC-1: GET /api/wecom/callback for verification
    Verification must return decrypted echostr.
    """
    if webhook_handler.verify_signature(msg_signature, timestamp, nonce, echostr):
        # In a real scenario, we would decrypt echostr.
        # For mock, we just return it.
        return Response(content=echostr, media_type="text/plain")
    else:
        raise HTTPException(status_code=403, detail="Invalid signature")

@router.post("/callback")
async def handle_webhook(
    request: Request,
    msg_signature: str,
    timestamp: str,
    nonce: str
):
    """
    AC-1: POST /api/wecom/callback for receiving messages
    Includes idempotency check.
    """
    body = await request.body()
    xml_payload = body.decode("utf-8")

    if not webhook_handler.verify_signature(msg_signature, timestamp, nonce):
        raise HTTPException(status_code=403, detail="Invalid signature")

    # Extract MsgId for idempotency check
    try:
        data = xmltodict.parse(xml_payload)
        if "xml" in data:
            data = data["xml"]
        msg_id = data.get("MsgId")

        if msg_id and webhook_handler.is_duplicate(msg_id):
            logger.info(f"Duplicate message received: {msg_id}, skipping.")
            return {"status": "ok", "detail": "duplicate"}

    except Exception as e:
        logger.warning(f"Failed to parse XML for idempotency check: {e}")

    await message_processor.process_webhook_payload(xml_payload)
    return {"status": "ok"}

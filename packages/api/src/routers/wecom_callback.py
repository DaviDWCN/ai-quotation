from fastapi import APIRouter, Request, Query, HTTPException, Depends
from fastapi.responses import PlainTextResponse
import logging
from src.services.wecom.webhook import WeComWebhookHandler
from src.services.wecom.mock_wecom import MockWeComAdapter
from src.services.wecom.message import WeComMessageHandler, get_message_handler

logger = logging.getLogger(__name__)

def get_wecom_webhook_handler() -> WeComWebhookHandler:
    return WeComWebhookHandler(MockWeComAdapter())

router = APIRouter(prefix="/api/wecom", tags=["wecom"])

@router.get("/callback", response_class=PlainTextResponse)
async def verify_url(
    msg_signature: str = Query(...),
    timestamp: str = Query(...),
    nonce: str = Query(...),
    echostr: str = Query(...),
    handler: WeComWebhookHandler = Depends(get_wecom_webhook_handler)
):
    try:
        result = await handler.verify(msg_signature, timestamp, nonce, echostr)
        return result
    except Exception as e:
        logger.error(f"Error verifying WeCom URL: {e}")
        raise HTTPException(status_code=400, detail="Verification failed")

@router.post("/callback")
async def handle_callback(
    request: Request,
    msg_signature: str = Query(...),
    timestamp: str = Query(...),
    nonce: str = Query(...),
    webhook_handler: WeComWebhookHandler = Depends(get_wecom_webhook_handler),
    message_handler: WeComMessageHandler = Depends(get_message_handler)
):
    data = await request.body()
    try:
        parsed_data = await webhook_handler.handle_callback(msg_signature, timestamp, nonce, data)
        await message_handler.process_message(parsed_data)
        return "ok"
    except Exception as e:
        logger.error(f"Error handling WeCom callback: {e}")
        raise HTTPException(status_code=400, detail="Callback handling failed")

import logging
import os
from typing import Any, Dict, Optional, Union

import xmltodict
from fastapi import HTTPException
from src.services.wecom.adapter import WeComAdapter
from src.services.wecom.message import (
    WeComFileMessage,
    WeComImageMessage,
    WeComMessageType,
    WeComTextMessage,
)

logger = logging.getLogger(__name__)

STORAGE_DIR = "storage/wecom"


def verify_signature(
    msg_signature: str, timestamp: str, nonce: str, echostr: Optional[str] = None
) -> Optional[str]:
    """
    Verify WeCom WebHook signature.
    In Mock mode, this can be bypassed or just return the echostr.
    """
    if echostr:
        return echostr
    return None


async def parse_xml_payload(xml_data: str) -> Dict[str, Any]:
    """Parse WeCom XML payload to dictionary."""
    try:
        parsed = xmltodict.parse(xml_data)
        return parsed.get("xml", {})  # type: ignore
    except Exception as e:
        logger.error(f"Failed to parse XML: {e}")
        raise HTTPException(status_code=400, detail="Invalid XML payload")


async def handle_webhook_request(
    payload: Dict[str, Any], adapter: Optional[WeComAdapter] = None
) -> Dict[str, Union[str, WeComTextMessage, WeComImageMessage, WeComFileMessage]]:
    """
    Process incoming WeCom messages.
    """
    msg_type = payload.get("MsgType")
    logger.info(f"Received WeCom message of type: {msg_type}")

    if msg_type == WeComMessageType.TEXT:
        return {"type": "text", "data": WeComTextMessage(**payload)}

    elif msg_type == WeComMessageType.IMAGE:
        msg_image = WeComImageMessage(**payload)
        if adapter:
            await download_and_save_media(adapter, msg_image.media_id, "image")
        return {"type": "image", "data": msg_image}

    elif msg_type == WeComMessageType.FILE:
        msg_file = WeComFileMessage(**payload)
        if adapter:
            await download_and_save_media(
                adapter, msg_file.media_id, "file", msg_file.file_name
            )
        return {"type": "file", "data": msg_file}

    else:
        logger.warning(f"Unsupported message type: {msg_type}")
        raise HTTPException(
            status_code=400, detail=f"Unsupported message type: {msg_type}"
        )


async def download_and_save_media(
    adapter: WeComAdapter, media_id: str, media_type: str, filename: Optional[str] = None
) -> str:
    """Download media from WeCom and save to local storage."""
    content = await adapter.get_media(media_id)
    os.makedirs(STORAGE_DIR, exist_ok=True)

    if not filename:
        filename = f"{media_type}_{media_id}"

    filepath = os.path.join(STORAGE_DIR, filename)
    with open(filepath, "wb") as f:
        f.write(content)

    logger.info(f"Saved {media_type} to {filepath}")
    return filepath

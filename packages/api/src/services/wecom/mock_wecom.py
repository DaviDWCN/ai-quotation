import logging
from typing import Any, Dict

from src.services.wecom.adapter import WeComAdapter

logger = logging.getLogger(__name__)


class MockWeComAdapter(WeComAdapter):
    """Mock implementation of WeComAdapter for testing and development."""

    async def send_message(self, user_id: str, content: Dict[str, Any]) -> Dict[str, Any]:
        """Mock sending a message."""
        logger.info(f"Mock sending message to user {user_id}: {content}")
        return {"errcode": 0, "errmsg": "ok", "msgid": "mock_msgid"}

    async def get_media(self, media_id: str) -> bytes:
        """Mock downloading media."""
        logger.info(f"Mock downloading media with id {media_id}")
        return b"mock_media_content"

from typing import Any, Dict, Protocol


class WeComAdapter(Protocol):
    """Protocol for WeCom API interactions."""

    async def send_message(self, user_id: str, content: Dict[str, Any]) -> Dict[str, Any]:
        """Send a message to a user."""
        ...

    async def get_media(self, media_id: str) -> bytes:
        """Download media from WeCom."""
        ...

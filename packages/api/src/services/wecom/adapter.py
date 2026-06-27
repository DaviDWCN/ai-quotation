from typing import Protocol, Any, Optional

class WeComAdapter(Protocol):
    async def send_text_message(self, user_id: str, content: str) -> None:
        """Send a text message to a user."""
        ...

    async def send_image_message(self, user_id: str, media_id: str) -> None:
        """Send an image message to a user."""
        ...

    async def send_file_message(self, user_id: str, media_id: str) -> None:
        """Send a file message to a user."""
        ...

    async def send_template_card(self, user_id: str, card_data: dict[str, Any]) -> None:
        """Send a template card message to a user."""
        ...

    async def download_media(self, media_id: str) -> bytes:
        """Download media from WeCom by media_id."""
        ...

    async def get_media_url(self, media_id: str) -> str:
        """Get the URL for a media file."""
        ...

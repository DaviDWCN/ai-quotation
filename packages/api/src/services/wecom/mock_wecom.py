from typing import Any, Dict, List
from .adapter import WeComAdapter

class MockWeComAdapter:
    def __init__(self) -> None:
        self.sent_messages: List[Dict[str, Any]] = []

    async def send_text_message(self, user_id: str, content: str) -> None:
        self.sent_messages.append({
            "type": "text",
            "user_id": user_id,
            "content": content
        })
        print(f"Mock WeCom: Sent text to {user_id}: {content}")

    async def send_image_message(self, user_id: str, media_id: str) -> None:
        self.sent_messages.append({
            "type": "image",
            "user_id": user_id,
            "media_id": media_id
        })
        print(f"Mock WeCom: Sent image to {user_id}: {media_id}")

    async def send_file_message(self, user_id: str, media_id: str) -> None:
        self.sent_messages.append({
            "type": "file",
            "user_id": user_id,
            "media_id": media_id
        })
        print(f"Mock WeCom: Sent file to {user_id}: {media_id}")

    async def send_template_card(self, user_id: str, card_data: dict[str, Any]) -> None:
        self.sent_messages.append({
            "type": "template_card",
            "user_id": user_id,
            "card_data": card_data
        })
        print(f"Mock WeCom: Sent card to {user_id}")

    async def download_media(self, media_id: str) -> bytes:
        # Return dummy content for mock
        return b"dummy content for " + media_id.encode()

    async def get_media_url(self, media_id: str) -> str:
        return f"https://mock.wecom.com/media/{media_id}"

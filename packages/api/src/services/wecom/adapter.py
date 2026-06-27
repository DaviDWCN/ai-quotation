from typing import Protocol, Optional

class WeComAdapter(Protocol):
    async def verify_webhook(self, signature: str, timestamp: str, nonce: str, echostr: str) -> str:
        """Verify the webhook signature and return the decrypted echostr."""
        ...

    async def decrypt_callback_data(self, signature: str, timestamp: str, nonce: str, data: bytes) -> str:
        """Decrypt the incoming callback data from WeCom."""
        ...

    async def download_media(self, media_id: str) -> bytes:
        """Download media (file/image) from WeCom."""
        ...

    async def send_approval_card(
        self,
        user_id: str,
        draft_id: str,
        customer_name: str,
        material_summary: str,
        jump_url: str
    ) -> None:
        """Send an approval card message to a user."""
        ...

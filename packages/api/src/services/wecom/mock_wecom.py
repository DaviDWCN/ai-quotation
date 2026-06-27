from .adapter import WeComAdapter

class MockWeComAdapter(WeComAdapter):
    async def verify_webhook(self, signature: str, timestamp: str, nonce: str, echostr: str) -> str:
        # Mock implementation simply returns echostr
        return echostr

    async def decrypt_callback_data(self, signature: str, timestamp: str, nonce: str, data: bytes) -> str:
        # Mock implementation returns data as string
        return data.decode("utf-8")

    async def download_media(self, media_id: str) -> bytes:
        # Mock implementation returns dummy bytes
        return b"mock_file_content"

    async def send_approval_card(
        self,
        user_id: str,
        draft_id: str,
        customer_name: str,
        material_summary: str,
        jump_url: str
    ) -> None:
        # Mock implementation prints the card details
        print(f"Mock sending approval card to {user_id} for draft {draft_id}")
        print(f"Customer: {customer_name}, Material: {material_summary}, URL: {jump_url}")

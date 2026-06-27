from typing import List, Optional, Dict
from .adapter import MailAdapter

class MockIMAPAdapter:
    def __init__(self) -> None:
        self.messages: Dict[str, bytes] = {}
        self.connected = False

    async def connect(self) -> None:
        self.connected = True

    async def disconnect(self) -> None:
        self.connected = False

    async def list_messages(self, folder: str = "INBOX") -> List[str]:
        if not self.connected:
            raise ConnectionError("Not connected")
        return list(self.messages.keys())

    async def fetch_message(self, message_id: str) -> Optional[bytes]:
        if not self.connected:
            raise ConnectionError("Not connected")
        return self.messages.get(message_id)

    async def mark_as_read(self, message_id: str) -> None:
        if not self.connected:
            raise ConnectionError("Not connected")
        # In mock, we might just log this
        pass

    def add_mock_message(self, message_id: str, content: bytes) -> None:
        self.messages[message_id] = content

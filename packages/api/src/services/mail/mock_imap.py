from typing import List
from .adapter import MailMessage, MailAdapter

class MockIMAPAdapter:
    def __init__(self) -> None:
        self.messages: List[MailMessage] = []
        self.connected = False

    async def connect(self) -> None:
        self.connected = True

    async def disconnect(self) -> None:
        self.connected = False

    async def fetch_new_messages(self) -> List[MailMessage]:
        if not self.connected:
            raise RuntimeError("Not connected")
        msgs = self.messages[:]
        self.messages.clear()
        return msgs

    async def mark_as_read(self, message_id: str) -> None:
        pass

    def add_mock_message(self, message: MailMessage) -> None:
        self.messages.append(message)

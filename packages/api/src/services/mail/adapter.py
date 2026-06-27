from typing import Protocol, List, Optional, Any

class MailAdapter(Protocol):
    async def connect(self) -> None:
        """Connect to the mail server."""
        ...

    async def disconnect(self) -> None:
        """Disconnect from the mail server."""
        ...

    async def list_messages(self, folder: str = "INBOX") -> List[str]:
        """List message IDs in a folder."""
        ...

    async def fetch_message(self, message_id: str) -> Optional[bytes]:
        """Fetch the raw content of a message."""
        ...

    async def mark_as_read(self, message_id: str) -> None:
        """Mark a message as read."""
        ...

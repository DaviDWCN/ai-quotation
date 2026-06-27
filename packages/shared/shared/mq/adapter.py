from typing import Any, Protocol

class MQAdapter(Protocol):
    async def connect(self) -> None:
        """Connect to the message queue."""
        ...

    async def disconnect(self) -> None:
        """Disconnect from the message queue."""
        ...

    async def publish(self, topic: str, message: Any) -> None:
        """Publish a message to a topic."""
        ...

    async def subscribe(self, topic: str, callback: Any) -> None:
        """Subscribe to a topic and execute callback on message."""
        ...

from typing import Protocol, Any
import abc

class NotificationService(abc.ABC):
    @abc.abstractmethod
    async def send_draft_notification(self, draft_id: str, customer_name: str, status: str) -> None:
        """Send a notification about a new draft."""
        pass

class WeComNotificationService(NotificationService):
    def __init__(self, webhook_url: str = ""):
        self.webhook_url = webhook_url

    async def send_draft_notification(self, draft_id: str, customer_name: str, status: str) -> None:
        # Implementation will call WeCom webhook or adapter
        # For now, we mock the notification
        print(f"NOTIFICATION: New draft {draft_id} for {customer_name} created. Status: {status}")
        # In a real implementation, this would use httpx to call WeCom API

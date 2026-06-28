import asyncio
import io
import logging
from datetime import datetime, timezone
from typing import Set
from .adapter import MailAdapter, MailMessage
from src.services.file_storage import FileStorageAdapter
from packages.shared.mq.adapter import MQAdapter
from src.config import settings

logger = logging.getLogger(__name__)

class MailListener:
    def __init__(
        self,
        mail_adapter: MailAdapter,
        storage_adapter: FileStorageAdapter,
        mq_adapter: MQAdapter,
        poll_interval: int = settings.mail_poll_interval
    ) -> None:
        self.mail_adapter = mail_adapter
        self.storage_adapter = storage_adapter
        self.mq_adapter = mq_adapter
        self.poll_interval = poll_interval
        self.processed_message_ids: Set[str] = set()
        self.is_running = False

    async def start(self) -> None:
        self.is_running = True
        await self.mail_adapter.connect()
        while self.is_running:
            try:
                await self.poll()
            except Exception as e:
                logger.error(f"Error during mail polling: {e}")
            await asyncio.sleep(self.poll_interval)

    async def stop(self) -> None:
        self.is_running = False
        await self.mail_adapter.disconnect()

    async def poll(self) -> None:
        messages = await self.mail_adapter.fetch_new_messages()
        for msg in messages:
            if msg.message_id in self.processed_message_ids:
                logger.info(f"Skipping already processed message: {msg.message_id}")
                continue

            try:
                await self.process_message(msg)
                self.processed_message_ids.add(msg.message_id)
            except Exception as e:
                logger.error(f"Failed to process message {msg.message_id}: {e}")
                # Publish to dead letter queue
                await self.mq_adapter.publish(
                    settings.mq_dead_letter_topic,
                    {"message_id": msg.message_id, "error": str(e)}
                )

    async def process_message(self, msg: MailMessage) -> None:
        attachment_urls = []
        for attachment in msg.attachments:
            # Check for size limits (AC-8)
            if len(attachment.content) > settings.mail_max_attachment_size:
                raise ValueError(f"Attachment {attachment.filename} exceeds size limit of {settings.mail_max_attachment_size} bytes")

            file_obj = io.BytesIO(attachment.content)
            url = await self.storage_adapter.upload_file(
                file_obj,
                f"{msg.message_id}_{attachment.filename}",
                attachment.content_type
            )
            attachment_urls.append(url)

        payload = {
            "message_id": msg.message_id,
            "sender": msg.sender,
            "subject": msg.subject,
            "body_text": msg.body_text,
            "body_html": msg.body_html,
            "attachments": attachment_urls,
            "received_at": datetime.now(timezone.utc).isoformat()
        }

        await self.mq_adapter.publish(
            settings.mq_quotation_parse_topic,
            payload
        )
        await self.mail_adapter.mark_as_read(msg.message_id)

import asyncio
import logging
import io
import uuid
from typing import Set, Optional
from .parser import EmailMessage
from .adapter import MailAdapter
from ..file_storage import FileStorageAdapter
from packages.shared.mq.adapter import MQAdapter

logger = logging.getLogger(__name__)

class MailListener:
    def __init__(
        self,
        mail_adapter: MailAdapter,
        file_storage: FileStorageAdapter,
        mq_adapter: MQAdapter,
        bucket_name: str,
        polling_interval: int = 30
    ):
        self.mail_adapter = mail_adapter
        self.file_storage = file_storage
        self.mq_adapter = mq_adapter
        self.bucket_name = bucket_name
        self.polling_interval = polling_interval
        self.processed_message_ids: Set[str] = set()
        self.is_running = False

    async def start(self) -> None:
        self.is_running = True
        self.mail_adapter.connect()
        logger.info("MailListener started")

        while self.is_running:
            try:
                await self.poll()
            except Exception as e:
                logger.error(f"Error during polling: {e}")
            await asyncio.sleep(self.polling_interval)

    def stop(self) -> None:
        self.is_running = False
        self.mail_adapter.disconnect()
        logger.info("MailListener stopped")

    async def poll(self) -> None:
        try:
            emails = await asyncio.to_thread(self.mail_adapter.fetch_new_emails)
        except Exception as e:
            logger.error(f"Error fetching emails: {e}. Attempting to reconnect...")
            try:
                await asyncio.to_thread(self.mail_adapter.connect)
                emails = await asyncio.to_thread(self.mail_adapter.fetch_new_emails)
            except Exception as re_e:
                logger.error(f"Reconnection failed: {re_e}")
                return

        for email in emails:
            if email.message_id in self.processed_message_ids:
                logger.info(f"Skipping duplicate email: {email.message_id}")
                continue

            try:
                await self.process_email(email)
                self.processed_message_ids.add(email.message_id)
            except Exception as e:
                logger.error(f"Failed to process email {email.message_id}: {e}")
                # In a real system, we'd send to DLQ here
                await self.mq_adapter.publish("quotation.dlq", {
                    "error": str(e),
                    "message_id": email.message_id,
                    "subject": email.subject
                })

    async def process_email(self, email: EmailMessage) -> None:
        logger.info(f"Processing email: {email.subject} from {email.sender}")

        # Upload attachments
        for attachment in email.attachments:
            object_name = f"{uuid.uuid4()}-{attachment.filename}"
            storage_path = await asyncio.to_thread(
                self.file_storage.upload_file,
                self.bucket_name,
                object_name,
                io.BytesIO(attachment.content),
                attachment.content_type
            )
            attachment.storage_path = storage_path
            # Clear content to reduce MQ message size if needed, but here we keep it or not?
            # Specification says "投递给 AI 解析引擎处理", usually better to send storage path.
            attachment.content = b""

        # Publish to MQ
        message_payload = email.model_dump()
        await self.mq_adapter.publish("quotation.parse", message_payload)
        logger.info(f"Published email {email.message_id} to MQ")

import imaplib
import logging
from typing import List, Optional, Set, Any, Dict, cast
import asyncio
from io import BytesIO

from .adapter import MailAdapter
from .parser import EmailParser
from ..file_storage import FileStorageAdapter
from shared.mq.adapter import MQAdapter

logger = logging.getLogger(__name__)

class IMAPAdapter:
    def __init__(self, host: str, port: int, user: str, password: str, use_ssl: bool = True):
        self.host = host
        self.port = port
        self.user = user
        self.password = password
        self.use_ssl = use_ssl
        self.imap: Optional[imaplib.IMAP4] = None

    async def connect(self) -> None:
        if self.use_ssl:
            self.imap = await asyncio.to_thread(imaplib.IMAP4_SSL, self.host, self.port)
        else:
            self.imap = await asyncio.to_thread(imaplib.IMAP4, self.host, self.port)

        await asyncio.to_thread(self.imap.login, self.user, self.password)

    async def disconnect(self) -> None:
        if self.imap:
            try:
                await asyncio.to_thread(self.imap.logout)
            except Exception:
                pass
            self.imap = None

    async def list_messages(self, folder: str = "INBOX") -> List[str]:
        if not self.imap:
            raise ConnectionError("Not connected")

        await asyncio.to_thread(self.imap.select, folder)
        # Search for UNSEEN messages for better performance and safety
        status, messages = await asyncio.to_thread(self.imap.search, None, 'UNSEEN')
        if status != 'OK':
            return []

        return cast(List[str], messages[0].decode().split())

    async def fetch_message(self, message_id: str) -> Optional[bytes]:
        if not self.imap:
            raise ConnectionError("Not connected")

        status, data = await asyncio.to_thread(self.imap.fetch, message_id, '(RFC822)')
        if status != 'OK':
            return None

        for response_part in data:
            if isinstance(response_part, tuple):
                return response_part[1]
        return None

    async def mark_as_read(self, message_id: str) -> None:
        if not self.imap:
            raise ConnectionError("Not connected")
        await asyncio.to_thread(self.imap.store, message_id, '+FLAGS', '\\Seen')


class MailListener:
    def __init__(
        self,
        mail_adapter: MailAdapter,
        storage_adapter: FileStorageAdapter,
        mq_adapter: MQAdapter,
        poll_interval: int = 30
    ):
        self.mail_adapter = mail_adapter
        self.storage_adapter = storage_adapter
        self.mq_adapter = mq_adapter
        self.poll_interval = poll_interval
        self.processed_message_ids: Set[str] = set()
        self.running = False

    async def start(self) -> None:
        self.running = True
        while self.running:
            try:
                await self.mail_adapter.connect()
                while self.running:
                    try:
                        await self.poll()
                    except (imaplib.IMAP4.error, ConnectionError, OSError) as e:
                        logger.error(f"IMAP connection lost: {e}. Attempting to reconnect...")
                        break # Break inner loop to reconnect
                    except Exception as e:
                        logger.error(f"Unexpected error during poll: {e}")
                    await asyncio.sleep(self.poll_interval)
            except Exception as e:
                logger.error(f"Failed to connect to mail server: {e}. Retrying in {self.poll_interval}s...")
                await asyncio.sleep(self.poll_interval)
            finally:
                await self.mail_adapter.disconnect()

    async def stop(self) -> None:
        self.running = False
        await self.mail_adapter.disconnect()

    async def poll(self) -> None:
        message_ids = await self.mail_adapter.list_messages()
        for msg_id in message_ids:
            raw_email = await self.mail_adapter.fetch_message(msg_id)
            if not raw_email:
                continue

            parser = EmailParser(raw_email)
            message_id_header = parser.get_message_id()

            if not message_id_header:
                logger.warning(f"Message {msg_id} has no Message-ID, skipping and marking as read.")
                await self.mail_adapter.mark_as_read(msg_id)
                continue

            if message_id_header in self.processed_message_ids:
                logger.info(f"Skipping duplicate message: {message_id_header}, marking as read.")
                await self.mail_adapter.mark_as_read(msg_id)
                continue

            try:
                email_data = parser.parse()

                attachment_urls = []
                for attachment in email_data["attachments"]:
                    file_obj = BytesIO(attachment["content"])
                    # Use a safe name for object path
                    safe_msg_id = message_id_header.replace("<", "").replace(">", "").replace("@", "_")
                    object_name = f"attachments/{safe_msg_id}/{attachment['filename']}"
                    url = await self.storage_adapter.upload_file(file_obj, "quotations", object_name)
                    attachment_urls.append({
                        "filename": attachment["filename"],
                        "url": url,
                        "content_type": attachment["content_type"]
                    })

                payload = {
                    "message_id": email_data["message_id"],
                    "subject": email_data["subject"],
                    "sender": email_data["sender"],
                    "to": email_data["to"],
                    "body_plain": email_data["body_plain"],
                    "body_html": email_data["body_html"],
                    "attachments": attachment_urls
                }

                await self.mq_adapter.publish("quotation.parse", payload)

                self.processed_message_ids.add(message_id_header)
                await self.mail_adapter.mark_as_read(msg_id)
                logger.info(f"Successfully processed message: {message_id_header}")

            except Exception as e:
                logger.error(f"Failed to process message {message_id_header}: {e}")
                error_payload = {
                    "message_id": message_id_header,
                    "error": str(e)
                }
                await self.mq_adapter.publish("quotation.dead_letter", error_payload)
                # Mark failed message as read to avoid infinite retry loop in poll
                await self.mail_adapter.mark_as_read(msg_id)

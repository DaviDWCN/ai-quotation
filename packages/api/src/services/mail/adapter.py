from typing import List, Optional, Protocol, BinaryIO
from pydantic import BaseModel, Field

class Attachment(BaseModel):
    filename: str
    content_type: str
    content: bytes

class MailMessage(BaseModel):
    message_id: str
    sender: str
    recipients: List[str]
    subject: str
    body_text: Optional[str] = None
    body_html: Optional[str] = None
    attachments: List[Attachment] = Field(default_factory=list)

class MailAdapter(Protocol):
    async def connect(self) -> None:
        ...

    async def disconnect(self) -> None:
        ...

    async def fetch_new_messages(self) -> List[MailMessage]:
        ...

    async def mark_as_read(self, message_id: str) -> None:
        ...

import imaplib
import email
import asyncio
from email.message import Message
from .parser import parse_email_message
from src.config import settings

class IMAPAdapter:
    def __init__(self) -> None:
        self.host = settings.imap_host
        self.port = settings.imap_port
        self.user = settings.imap_user
        self.password = settings.imap_password
        self.use_ssl = settings.imap_use_ssl
        self.mailbox = settings.imap_mailbox
        self.connection: Optional[imaplib.IMAP4_SSL | imaplib.IMAP4] = None
        self.msg_id_map: dict[str, str] = {} # message_id -> msg_num

    async def connect(self) -> None:
        if self.use_ssl:
            self.connection = await asyncio.to_thread(imaplib.IMAP4_SSL, self.host, self.port)
        else:
            self.connection = await asyncio.to_thread(imaplib.IMAP4, self.host, self.port)

        await asyncio.to_thread(self.connection.login, self.user, self.password)
        await asyncio.to_thread(self.connection.select, self.mailbox)

    async def disconnect(self) -> None:
        if self.connection:
            await asyncio.to_thread(self.connection.close)
            await asyncio.to_thread(self.connection.logout)
            self.connection = None

    async def fetch_new_messages(self) -> List[MailMessage]:
        if not self.connection:
            raise RuntimeError("Not connected to IMAP server")

        # Search for unseen messages
        status, messages = await asyncio.to_thread(self.connection.search, None, "UNSEEN")
        if status != "OK":
            return []

        mail_messages = []
        self.msg_id_map.clear()
        for msg_num_bytes in messages[0].split():
            msg_num = msg_num_bytes.decode()
            # Fetch only headers first to check message-id, or fetch full for simplicity
            # To avoid marking as read prematurely, we can use PEEK
            status, data = await asyncio.to_thread(self.connection.fetch, msg_num, "(BODY.PEEK[])")
            if status != "OK":
                continue

            raw_email = data[0][1] # type: ignore
            if isinstance(raw_email, bytes):
                msg = email.message_from_bytes(raw_email)
                mail_message = parse_email_message(msg)
                mail_messages.append(mail_message)
                self.msg_id_map[mail_message.message_id] = msg_num

        return mail_messages

    async def mark_as_read(self, message_id: str) -> None:
        if not self.connection:
            return

        msg_num = self.msg_id_map.get(message_id)
        if msg_num:
            await asyncio.to_thread(self.connection.store, msg_num, "+FLAGS", "\\Seen")

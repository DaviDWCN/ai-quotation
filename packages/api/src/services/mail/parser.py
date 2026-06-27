import email
from email.message import Message
from typing import List, Optional
from pydantic import BaseModel, Field

class Attachment(BaseModel):
    filename: str
    content_type: str
    content: bytes
    size: int
    storage_path: Optional[str] = None

class EmailMessage(BaseModel):
    message_id: str
    subject: str
    sender: str
    recipient: str
    body_text: str = ""
    body_html: str = ""
    attachments: List[Attachment] = Field(default_factory=list)
    received_at: str

class MailParser:
    @staticmethod
    def parse_email(raw_email: bytes) -> EmailMessage:
        msg = email.message_from_bytes(raw_email)

        message_id = msg.get("Message-ID", "")
        subject = msg.get("Subject", "")
        sender = msg.get("From", "")
        recipient = msg.get("To", "")
        received_at = msg.get("Date", "")

        body_text = ""
        body_html = ""
        attachments = []

        if msg.is_multipart():
            for part in msg.walk():
                content_type = part.get_content_type()
                content_disposition = str(part.get("Content-Disposition"))

                if content_type == "text/plain" and "attachment" not in content_disposition:
                    payload = part.get_payload(decode=True)
                    if isinstance(payload, bytes):
                        body_text += payload.decode(part.get_content_charset() or "utf-8", errors="replace")
                elif content_type == "text/html" and "attachment" not in content_disposition:
                    payload = part.get_payload(decode=True)
                    if isinstance(payload, bytes):
                        body_html += payload.decode(part.get_content_charset() or "utf-8", errors="replace")
                elif "attachment" in content_disposition:
                    filename = part.get_filename()
                    if filename:
                        payload = part.get_payload(decode=True)
                        if isinstance(payload, bytes):
                            attachments.append(Attachment(
                                filename=filename,
                                content_type=content_type,
                                content=payload,
                                size=len(payload)
                            ))
        else:
            payload = msg.get_payload(decode=True)
            if isinstance(payload, bytes):
                body_text = payload.decode(msg.get_content_charset() or "utf-8", errors="replace")

        return EmailMessage(
            message_id=message_id,
            subject=subject,
            sender=sender,
            recipient=recipient,
            body_text=body_text,
            body_html=body_html,
            attachments=attachments,
            received_at=received_at
        )

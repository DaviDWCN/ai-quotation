import email
from email.message import Message
from typing import List, Optional
from .adapter import MailMessage, Attachment

def parse_email_message(msg: Message) -> MailMessage:
    message_id = msg.get("Message-ID", "")
    sender = msg.get("From", "")
    subject = msg.get("Subject", "")

    # Recipients can be multiple
    to_headers = msg.get_all("To", [])
    cc_headers = msg.get_all("Cc", [])
    recipients = []
    for header in to_headers + cc_headers:
        recipients.extend([r.strip() for r in header.split(",")])

    body_text = None
    body_html = None
    attachments = []

    if msg.is_multipart():
        for part in msg.walk():
            content_type = part.get_content_type()
            content_disposition = str(part.get("Content-Disposition"))

            if content_type == "text/plain" and "attachment" not in content_disposition:
                payload = part.get_payload(decode=True)
                if isinstance(payload, bytes):
                    body_text = payload.decode(part.get_content_charset() or "utf-8", errors="replace")
            elif content_type == "text/html" and "attachment" not in content_disposition:
                payload = part.get_payload(decode=True)
                if isinstance(payload, bytes):
                    body_html = payload.decode(part.get_content_charset() or "utf-8", errors="replace")
            elif "attachment" in content_disposition:
                filename = part.get_filename()
                if filename:
                    payload = part.get_payload(decode=True)
                    if isinstance(payload, bytes):
                        attachments.append(Attachment(
                            filename=filename,
                            content_type=content_type,
                            content=payload
                        ))
    else:
        content_type = msg.get_content_type()
        payload = msg.get_payload(decode=True)
        if isinstance(payload, bytes):
            if content_type == "text/plain":
                body_text = payload.decode(msg.get_content_charset() or "utf-8", errors="replace")
            elif content_type == "text/html":
                body_html = payload.decode(msg.get_content_charset() or "utf-8", errors="replace")

    return MailMessage(
        message_id=message_id,
        sender=sender,
        recipients=recipients,
        subject=subject,
        body_text=body_text,
        body_html=body_html,
        attachments=attachments
    )

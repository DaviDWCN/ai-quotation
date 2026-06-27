import email
from email.message import Message
from typing import List, Dict, Optional, Any, cast

class EmailParser:
    def __init__(self, raw_email: bytes):
        self.message: Message = email.message_from_bytes(raw_email)

    def get_message_id(self) -> str:
        return cast(str, self.message.get("Message-ID", ""))

    def parse(self) -> Dict[str, Any]:
        """Parse the email and return a dictionary with extracted data."""
        subject = self.message.get("Subject", "")
        sender = self.message.get("From", "")
        to = self.message.get("To", "")

        body_plain = ""
        body_html = ""
        attachments = []

        if self.message.is_multipart():
            for part in self.message.walk():
                content_type = part.get_content_type()
                content_disposition = str(part.get("Content-Disposition"))

                if content_type == "text/plain" and "attachment" not in content_disposition:
                    payload = part.get_payload(decode=True)
                    if isinstance(payload, bytes):
                        body_plain += payload.decode(part.get_content_charset() or 'utf-8', errors='replace')
                elif content_type == "text/html" and "attachment" not in content_disposition:
                    payload = part.get_payload(decode=True)
                    if isinstance(payload, bytes):
                        body_html += payload.decode(part.get_content_charset() or 'utf-8', errors='replace')
                elif "attachment" in content_disposition:
                    filename = part.get_filename()
                    if filename:
                        payload = part.get_payload(decode=True)
                        if isinstance(payload, bytes):
                            attachments.append({
                                "filename": filename,
                                "content": payload,
                                "content_type": content_type
                            })
        else:
            payload = self.message.get_payload(decode=True)
            if isinstance(payload, bytes):
                content_type = self.message.get_content_type()
                decoded_body = payload.decode(self.message.get_content_charset() or 'utf-8', errors='replace')
                if content_type == "text/html":
                    body_html = decoded_body
                else:
                    body_plain = decoded_body

        return {
            "message_id": self.get_message_id(),
            "subject": subject,
            "sender": sender,
            "to": to,
            "body_plain": body_plain,
            "body_html": body_html,
            "attachments": attachments
        }

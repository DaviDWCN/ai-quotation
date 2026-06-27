import imaplib
from typing import List, Protocol, Optional
from .parser import EmailMessage, MailParser

class MailAdapter(Protocol):
    def connect(self) -> None:
        ...
    def disconnect(self) -> None:
        ...
    def fetch_new_emails(self) -> List[EmailMessage]:
        ...

class IMAPAdapter:
    def __init__(self, host: str, port: int, user: str, password: str, use_ssl: bool = True):
        self.host = host
        self.port = port
        self.user = user
        self.password = password
        self.use_ssl = use_ssl
        self.connection: Optional[imaplib.IMAP4] = None

    def connect(self) -> None:
        if self.use_ssl:
            self.connection = imaplib.IMAP4_SSL(self.host, self.port)
        else:
            self.connection = imaplib.IMAP4(self.host, self.port)
        self.connection.login(self.user, self.password)

    def disconnect(self) -> None:
        if self.connection:
            self.connection.logout()
            self.connection = None

    def fetch_new_emails(self) -> List[EmailMessage]:
        if not self.connection:
            raise Exception("Not connected to IMAP server")

        self.connection.select("INBOX")
        status, messages = self.connection.search(None, "UNSEEN")

        email_messages = []
        if status == "OK":
            for num in messages[0].split():
                status, data = self.connection.fetch(num, "(RFC822)")
                if status == "OK":
                    raw_email = data[0][1] # type: ignore
                    if isinstance(raw_email, bytes):
                        email_messages.append(MailParser.parse_email(raw_email))

        return email_messages

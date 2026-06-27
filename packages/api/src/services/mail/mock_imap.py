from typing import List
from .parser import EmailMessage
from .adapter import MailAdapter

class MockMailAdapter:
    def __init__(self) -> None:
        self.mock_emails: List[EmailMessage] = []
        self.connected = False

    def connect(self) -> None:
        self.connected = True

    def disconnect(self) -> None:
        self.connected = False

    def fetch_new_emails(self) -> List[EmailMessage]:
        if not self.connected:
            raise Exception("Not connected")
        emails = self.mock_emails[:]
        self.mock_emails = [] # Clear after fetch to simulate "UNSEEN"
        return emails

    def add_mock_email(self, email: EmailMessage) -> None:
        self.mock_emails.append(email)

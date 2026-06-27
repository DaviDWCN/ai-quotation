import pytest
import asyncio
from unittest.mock import MagicMock, AsyncMock
from src.services.mail.listener import MailListener
from src.services.mail.mock_imap import MockMailAdapter
from src.services.mail.parser import MailParser, EmailMessage, Attachment

@pytest.fixture
def sample_email_bytes():
    with open("tests/fixtures/sample_email.eml", "rb") as f:
        return f.read()

def test_mail_parser(sample_email_bytes):
    email_msg = MailParser.parse_email(sample_email_bytes)
    assert email_msg.subject == "Test Quotation"
    assert email_msg.sender == "sender@example.com"
    assert email_msg.recipient == "recipient@example.com"
    assert "Hello, this is a test email body." in email_msg.body_text
    assert len(email_msg.attachments) == 1
    assert email_msg.attachments[0].filename == "quotation.pdf"

@pytest.mark.asyncio
async def test_mail_listener_polling():
    mail_adapter = MockMailAdapter()
    file_storage = MagicMock()
    file_storage.upload_file.return_value = "bucket/path"
    mq_adapter = AsyncMock()

    listener = MailListener(
        mail_adapter=mail_adapter,
        file_storage=file_storage,
        mq_adapter=mq_adapter,
        bucket_name="test-bucket",
        polling_interval=1
    )

    # Mock an email
    email = EmailMessage(
        message_id="unique-123",
        subject="Request",
        sender="client@test.com",
        recipient="sales@company.com",
        body_text="Pls quote",
        attachments=[
            Attachment(filename="list.csv", content_type="text/csv", content=b"item,qty\napple,1", size=15)
        ],
        received_at="now"
    )
    mail_adapter.add_mock_email(email)
    mail_adapter.connect()

    await listener.poll()

    # Verify file storage was called
    assert file_storage.upload_file.called

    # Verify MQ publish was called
    mq_adapter.publish.assert_called_once()
    args, kwargs = mq_adapter.publish.call_args
    assert args[0] == "quotation.parse"
    assert args[1]["message_id"] == "unique-123"

    # Test idempotency
    mail_adapter.add_mock_email(email)
    await listener.poll()
    # MQ publish should NOT be called again for the same message_id
    assert mq_adapter.publish.call_count == 1

@pytest.mark.asyncio
async def test_mail_listener_error_handling():
    mail_adapter = MockMailAdapter()
    file_storage = MagicMock()
    file_storage.upload_file.side_effect = Exception("Upload failed")
    mq_adapter = AsyncMock()

    listener = MailListener(
        mail_adapter=mail_adapter,
        file_storage=file_storage,
        mq_adapter=mq_adapter,
        bucket_name="test-bucket"
    )

    email = EmailMessage(
        message_id="fail-123",
        subject="Fail",
        sender="client@test.com",
        recipient="sales@company.com",
        body_text="error",
        attachments=[Attachment(filename="x.txt", content_type="text/plain", content=b"x", size=1)],
        received_at="now"
    )
    mail_adapter.add_mock_email(email)
    mail_adapter.connect()

    await listener.poll()

    # Verify published to DLQ
    mq_adapter.publish.assert_called_once()
    args, kwargs = mq_adapter.publish.call_args
    assert args[0] == "quotation.dlq"

import pytest
import asyncio
from unittest.mock import MagicMock, AsyncMock, ANY
from src.services.mail.listener import MailListener
from src.services.mail.mock_imap import MockIMAPAdapter
from src.services.mail.parser import EmailParser
from src.services.file_storage import S3StorageAdapter
from shared.mq.adapter import MQAdapter

@pytest.fixture
def sample_email_content():
    with open("tests/fixtures/sample_email.eml", "rb") as f:
        return f.read()

@pytest.mark.asyncio
async def test_mail_listener_poll(sample_email_content):
    # Setup mocks
    mock_mail_adapter = MockIMAPAdapter()
    mock_mail_adapter.add_mock_message("1", sample_email_content)
    await mock_mail_adapter.connect()

    mock_storage_adapter = MagicMock(spec=S3StorageAdapter)
    mock_storage_adapter.upload_file = AsyncMock(return_value="bucket/path")

    mock_mq_adapter = MagicMock(spec=MQAdapter)
    mock_mq_adapter.publish = AsyncMock()

    listener = MailListener(
        mail_adapter=mock_mail_adapter,
        storage_adapter=mock_storage_adapter,
        mq_adapter=mock_mq_adapter,
        poll_interval=1
    )

    # Initial poll
    await listener.poll()

    # Check if message was processed (deduplication check)
    assert "<test-123@example.com>" in listener.processed_message_ids

    # Check if MQ publish was called
    mock_mq_adapter.publish.assert_called_with("quotation.parse", ANY)

    # Check if poll skips already processed message
    mock_mq_adapter.publish.reset_mock()
    await listener.poll()
    mock_mq_adapter.publish.assert_not_called()

@pytest.mark.asyncio
async def test_email_parser(sample_email_content):
    parser = EmailParser(sample_email_content)
    data = parser.parse()

    assert data["message_id"] == "<test-123@example.com>"
    assert data["subject"] == "Test Quotation Email"
    assert data["sender"] == "sender@example.com"
    assert len(data["attachments"]) == 1
    assert data["attachments"][0]["filename"] == "quotation.pdf"

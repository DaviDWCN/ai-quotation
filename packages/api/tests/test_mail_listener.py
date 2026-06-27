import pytest
import io
import email
from unittest.mock import AsyncMock, MagicMock
from src.services.mail.listener import MailListener
from src.services.mail.mock_imap import MockIMAPAdapter
from src.services.mail.adapter import MailMessage, Attachment
from src.services.mail.parser import parse_email_message

@pytest.fixture
def mock_storage():
    storage = AsyncMock()
    storage.upload_file.return_value = "s3://bucket/test.txt"
    return storage

@pytest.fixture
def mock_mq():
    mq = AsyncMock()
    return mq

@pytest.fixture
def mock_mail_adapter():
    return MockIMAPAdapter()

@pytest.mark.asyncio
async def test_mail_listener_poll_and_process(mock_mail_adapter, mock_storage, mock_mq):
    listener = MailListener(
        mail_adapter=mock_mail_adapter,
        storage_adapter=mock_storage,
        mq_adapter=mock_mq,
        poll_interval=1
    )

    # Add a mock message
    msg = MailMessage(
        message_id="msg-1",
        sender="sender@test.com",
        recipients=["to@test.com"],
        subject="Test Subject",
        body_text="Test Body",
        attachments=[
            Attachment(filename="test.txt", content_type="text/plain", content=b"hello")
        ]
    )
    mock_mail_adapter.add_mock_message(msg)

    await mock_mail_adapter.connect()
    await listener.poll()

    # Verify storage upload
    assert mock_storage.upload_file.called

    # Verify MQ publication
    assert mock_mq.publish.called
    args, kwargs = mock_mq.publish.call_args_list[0]
    assert args[0] == "quotation.parse"
    assert args[1]["message_id"] == "msg-1"
    assert args[1]["sender"] == "sender@test.com"
    assert "s3://bucket/test.txt" in args[1]["attachments"]

@pytest.mark.asyncio
async def test_mail_listener_deduplication(mock_mail_adapter, mock_storage, mock_mq):
    listener = MailListener(
        mail_adapter=mock_mail_adapter,
        storage_adapter=mock_storage,
        mq_adapter=mock_mq,
        poll_interval=1
    )

    msg = MailMessage(
        message_id="msg-1",
        sender="sender@test.com",
        recipients=["to@test.com"],
        subject="Test Subject",
        body_text="Test Body",
        attachments=[]
    )

    await mock_mail_adapter.connect()

    # First poll
    mock_mail_adapter.add_mock_message(msg)
    await listener.poll()
    assert mock_mq.publish.call_count == 1

    # Second poll with same message
    mock_mail_adapter.add_mock_message(msg)
    await listener.poll()
    assert mock_mq.publish.call_count == 1 # Should still be 1 due to de-duplication

def test_parse_email_from_fixture():
    with open("tests/fixtures/sample_email.eml", "rb") as f:
        msg_bytes = f.read()

    msg = email.message_from_bytes(msg_bytes)
    mail_message = parse_email_message(msg)

    assert mail_message.message_id == "<test-123@example.com>"
    assert mail_message.sender == "sender@example.com"
    assert "inquiry@company.com" in mail_message.recipients
    assert mail_message.subject == "Quote request for parts"
    assert "Please provide a quote" in mail_message.body_text
    assert len(mail_message.attachments) == 1
    assert mail_message.attachments[0].filename == "request.txt"
    assert mail_message.attachments[0].content == b"Part A: 10 units\nPart B: 5 units"

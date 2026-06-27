import pytest
from fastapi.testclient import TestClient
from src.main import app
from unittest.mock import MagicMock, AsyncMock, patch
import os

client = TestClient(app)

def test_verify_url():
    params = {
        "msg_signature": "sig",
        "timestamp": "123",
        "nonce": "nonce",
        "echostr": "hello"
    }
    response = client.get("/api/wecom/callback", params=params)
    assert response.status_code == 200
    # Verification should be plain text, not JSON
    assert response.text == "hello"

@patch("shared.mq.RabbitMQAdapter.publish", new_callable=AsyncMock)
def test_handle_text_callback(mock_publish):
    xml_data = """<xml>
        <ToUserName><![CDATA[toUser]]></ToUserName>
        <FromUserName><![CDATA[fromUser]]></FromUserName>
        <CreateTime>1348831860</CreateTime>
        <MsgType><![CDATA[text]]></MsgType>
        <Content><![CDATA[this is a test]]></Content>
        <MsgId>1234567890123456</MsgId>
    </xml>"""
    params = {
        "msg_signature": "sig",
        "timestamp": "123",
        "nonce": "nonce"
    }
    response = client.post("/api/wecom/callback", params=params, content=xml_data.encode("utf-8"))
    assert response.status_code == 200
    assert response.json() == "ok"

    mock_publish.assert_called_once()
    args, _ = mock_publish.call_args
    assert args[0] == "quotation.parse"
    assert args[1]["msg_type"] == "text"
    assert args[1]["content"] == "this is a test"

@patch("shared.mq.RabbitMQAdapter.publish", new_callable=AsyncMock)
@patch("src.services.wecom.mock_wecom.MockWeComAdapter.download_media", new_callable=AsyncMock)
def test_handle_file_callback(mock_download, mock_publish):
    mock_download.return_value = b"test content"
    xml_data = """<xml>
        <ToUserName><![CDATA[toUser]]></ToUserName>
        <FromUserName><![CDATA[fromUser]]></FromUserName>
        <CreateTime>1348831860</CreateTime>
        <MsgType><![CDATA[file]]></MsgType>
        <MediaId><![CDATA[media_id_123]]></MediaId>
        <FileName><![CDATA[test.pdf]]></FileName>
        <MsgId>1234567890123456</MsgId>
    </xml>"""
    params = {
        "msg_signature": "sig",
        "timestamp": "123",
        "nonce": "nonce"
    }
    response = client.post("/api/wecom/callback", params=params, content=xml_data.encode("utf-8"))
    assert response.status_code == 200

    mock_publish.assert_called_once()
    args, _ = mock_publish.call_args
    assert args[1]["msg_type"] == "file"
    assert "file_path" in args[1]
    assert args[1]["file_name"] == "test.pdf"

    # Check if file is saved
    file_path = args[1]["file_path"]
    assert os.path.exists(file_path)
    with open(file_path, "rb") as f:
        assert f.read() == b"test content"

    # Cleanup
    if os.path.exists(file_path):
        os.remove(file_path)

@patch("shared.mq.RabbitMQAdapter.publish", new_callable=AsyncMock)
@patch("src.services.wecom.mock_wecom.MockWeComAdapter.download_media", new_callable=AsyncMock)
def test_handle_file_callback_path_traversal(mock_download, mock_publish):
    mock_download.return_value = b"test content"
    xml_data = """<xml>
        <ToUserName><![CDATA[toUser]]></ToUserName>
        <FromUserName><![CDATA[fromUser]]></FromUserName>
        <CreateTime>1348831860</CreateTime>
        <MsgType><![CDATA[file]]></MsgType>
        <MediaId><![CDATA[media_id_evil]]></MediaId>
        <FileName><![CDATA[../../../tmp/evil.txt]]></FileName>
        <MsgId>1234567890123456</MsgId>
    </xml>"""
    params = {
        "msg_signature": "sig",
        "timestamp": "123",
        "nonce": "nonce"
    }
    response = client.post("/api/wecom/callback", params=params, content=xml_data.encode("utf-8"))
    assert response.status_code == 200

    args, _ = mock_publish.call_args
    file_path = args[1]["file_path"]
    file_name = args[1]["file_name"]

    assert file_name == "evil.txt"
    assert not file_path.endswith("../../../tmp/evil.txt")
    assert os.path.basename(file_path) == "evil.txt"

    # Cleanup
    if os.path.exists(file_path):
        os.remove(file_path)

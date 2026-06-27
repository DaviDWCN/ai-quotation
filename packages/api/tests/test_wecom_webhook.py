import pytest
from fastapi.testclient import TestClient
from src.main import app
import os
import shutil

client = TestClient(app)

@pytest.fixture(autouse=True)
def setup_storage():
    storage_dir = "packages/api/storage/wecom/"
    if os.path.exists(storage_dir):
        shutil.rmtree(storage_dir)
    os.makedirs(storage_dir)
    yield
    if os.path.exists(storage_dir):
        shutil.rmtree(storage_dir)

def test_wecom_webhook_verification():
    response = client.get(
        "/api/wecom/callback",
        params={
            "msg_signature": "mock",
            "timestamp": "123456",
            "nonce": "nonce",
            "echostr": "hello"
        }
    )
    assert response.status_code == 200
    assert response.text == "hello"

def test_wecom_webhook_text_message():
    xml_payload = """
    <xml>
      <ToUserName><![CDATA[toUser]]></ToUserName>
      <FromUserName><![CDATA[fromUser]]></FromUserName>
      <CreateTime>1348831860</CreateTime>
      <MsgType><![CDATA[text]]></MsgType>
      <Content><![CDATA[this is a test]]></Content>
      <MsgId>1234567890123456</MsgId>
      <AgentID>1</AgentID>
    </xml>
    """
    response = client.post(
        "/api/wecom/callback",
        params={
            "msg_signature": "mock",
            "timestamp": "123456",
            "nonce": "nonce"
        },
        content=xml_payload
    )
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}

def test_wecom_webhook_file_message():
    xml_payload = """
    <xml>
      <ToUserName><![CDATA[toUser]]></ToUserName>
      <FromUserName><![CDATA[fromUser]]></FromUserName>
      <CreateTime>1348831860</CreateTime>
      <MsgType><![CDATA[file]]></MsgType>
      <MediaId><![CDATA[media_id_123]]></MediaId>
      <FileName><![CDATA[test.pdf]]></FileName>
      <MsgId>1234567890123457</MsgId>
      <AgentID>1</AgentID>
    </xml>
    """
    response = client.post(
        "/api/wecom/callback",
        params={
            "msg_signature": "mock",
            "timestamp": "123456",
            "nonce": "nonce"
        },
        content=xml_payload
    )
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}
    # Check if file was "stored"
    assert os.path.exists("packages/api/storage/wecom/test.pdf")

def test_wecom_webhook_image_message():
    xml_payload = """
    <xml>
      <ToUserName><![CDATA[toUser]]></ToUserName>
      <FromUserName><![CDATA[fromUser]]></FromUserName>
      <CreateTime>1348831860</CreateTime>
      <MsgType><![CDATA[image]]></MsgType>
      <PicUrl><![CDATA[this is a url]]></PicUrl>
      <MediaId><![CDATA[media_id_456]]></MediaId>
      <MsgId>1234567890123458</MsgId>
      <AgentID>1</AgentID>
    </xml>
    """
    response = client.post(
        "/api/wecom/callback",
        params={
            "msg_signature": "mock",
            "timestamp": "123456",
            "nonce": "nonce"
        },
        content=xml_payload
    )
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}
    # Check if image was "stored"
    assert os.path.exists("packages/api/storage/wecom/media_id_456.jpg")

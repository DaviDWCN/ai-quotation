import pytest
import os
from fastapi.testclient import TestClient
from src.main import app

client = TestClient(app)


def test_wecom_verify() -> None:
    response = client.get(
        "/api/wecom/callback",
        params={
            "msg_signature": "sig",
            "timestamp": "123456",
            "nonce": "nonce",
            "echostr": "hello",
        },
    )
    assert response.status_code == 200
    assert response.text == "hello"


def test_wecom_callback_text() -> None:
    xml_payload = """
    <xml>
        <ToUserName><![CDATA[wxid]]></ToUserName>
        <FromUserName><![CDATA[userid]]></FromUserName>
        <CreateTime>123456</CreateTime>
        <MsgType><![CDATA[text]]></MsgType>
        <Content><![CDATA[hello world]]></Content>
        <MsgId>msg123</MsgId>
    </xml>
    """
    response = client.post(
        "/api/wecom/callback",
        params={"msg_signature": "sig", "timestamp": "123456", "nonce": "nonce"},
        content=xml_payload,
    )
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


def test_wecom_callback_file() -> None:
    xml_payload = """
    <xml>
        <ToUserName><![CDATA[wxid]]></ToUserName>
        <FromUserName><![CDATA[userid]]></FromUserName>
        <CreateTime>123456</CreateTime>
        <MsgType><![CDATA[file]]></MsgType>
        <FileName><![CDATA[test.pdf]]></FileName>
        <FileExt><![CDATA[pdf]]></FileExt>
        <MediaId><![CDATA[media_file_123]]></MediaId>
        <FileSize>1024</FileSize>
        <MsgId>msg_file_123</MsgId>
    </xml>
    """
    response = client.post(
        "/api/wecom/callback",
        params={"msg_signature": "sig", "timestamp": "123456", "nonce": "nonce"},
        content=xml_payload,
    )
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}

    # Verify file was "saved"
    assert os.path.exists("storage/wecom/test.pdf")


def test_wecom_callback_idempotency() -> None:
    xml_payload = """
    <xml>
        <ToUserName><![CDATA[wxid]]></ToUserName>
        <FromUserName><![CDATA[userid]]></FromUserName>
        <CreateTime>123456</CreateTime>
        <MsgType><![CDATA[text]]></MsgType>
        <Content><![CDATA[hello world]]></Content>
        <MsgId>msg_idempotent</MsgId>
    </xml>
    """
    # First call
    response1 = client.post(
        "/api/wecom/callback",
        params={"msg_signature": "sig", "timestamp": "123456", "nonce": "nonce"},
        content=xml_payload,
    )
    assert response1.status_code == 200

    # Second call
    response2 = client.post(
        "/api/wecom/callback",
        params={"msg_signature": "sig", "timestamp": "123456", "nonce": "nonce"},
        content=xml_payload,
    )
    assert response2.status_code == 200
    assert response2.json() == {"status": "ok"}

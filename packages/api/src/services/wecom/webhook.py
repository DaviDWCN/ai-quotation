import xml.etree.ElementTree as ET
from typing import Optional, Dict, Any
from .adapter import WeComAdapter

class WeComWebhookHandler:
    def __init__(self, adapter: WeComAdapter):
        self.adapter = adapter

    async def verify(self, signature: str, timestamp: str, nonce: str, echostr: str) -> str:
        return await self.adapter.verify_webhook(signature, timestamp, nonce, echostr)

    async def handle_callback(self, signature: str, timestamp: str, nonce: str, data: bytes) -> Dict[str, Any]:
        xml_content = await self.adapter.decrypt_callback_data(signature, timestamp, nonce, data)
        return self._parse_xml(xml_content)

    def _parse_xml(self, xml_content: str) -> Dict[str, Any]:
        root = ET.fromstring(xml_content)
        result = {}
        for child in root:
            result[child.tag] = child.text
        return result

import os
import logging
from typing import Dict, Any
from .adapter import WeComAdapter
from packages.shared.mq.adapter import MQAdapter

logger = logging.getLogger(__name__)

class WeComMessageHandler:
    def __init__(self, wecom_adapter: WeComAdapter, mq_adapter: MQAdapter):
        self.wecom_adapter = wecom_adapter
        self.mq_adapter = mq_adapter
        self.storage_path = os.getenv("FILE_STORAGE_PATH", "/tmp/wecom_media")
        os.makedirs(self.storage_path, exist_ok=True)

    async def process_message(self, data: Dict[str, Any]) -> None:
        msg_type = data.get("MsgType")
        conversation_id = data.get("FromUserName")

        message_payload = {
            "conversation_id": conversation_id,
            "msg_type": msg_type,
            "raw_data": data
        }

        if msg_type == "text":
            message_payload["content"] = data.get("Content")
        elif msg_type in ["file", "image"]:
            media_id = data.get("MediaId")
            if media_id:
                file_content = await self.wecom_adapter.download_media(media_id)
                # Sanitize filename to prevent path traversal
                raw_file_name = data.get("FileName", f"{media_id}")
                file_name = os.path.basename(raw_file_name)

                if msg_type == "image":
                    file_name = f"{media_id}.jpg"

                saved_path = self._save_file(file_name, file_content)
                message_payload["file_path"] = saved_path
                message_payload["file_name"] = file_name

        # Publish to MQ
        await self.mq_adapter.publish("quotation.parse", message_payload)

    def _save_file(self, file_name: str, content: bytes) -> str:
        # Extra precaution for filename
        safe_file_name = os.path.basename(file_name)
        file_path = os.path.join(self.storage_path, safe_file_name)
        with open(file_path, "wb") as f:
            f.write(content)
        return file_path

# Factory for the handler to be used as a dependency
def get_message_handler() -> WeComMessageHandler:
    from .mock_wecom import MockWeComAdapter
    from packages.shared.mq.rabbitmq import RabbitMQAdapter
    return WeComMessageHandler(
        MockWeComAdapter(),
        RabbitMQAdapter("mock://localhost")
    )

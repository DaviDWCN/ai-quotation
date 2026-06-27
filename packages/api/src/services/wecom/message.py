import io
import logging
from typing import Any, Dict, Optional
import xmltodict
from .adapter import WeComAdapter
from ..storage.adapter import FileStorageAdapter
from packages.shared.mq.adapter import MQAdapter

logger = logging.getLogger(__name__)

class MessageProcessor:
    def __init__(
        self,
        wecom_adapter: WeComAdapter,
        storage_adapter: FileStorageAdapter,
        mq_adapter: MQAdapter
    ):
        self.wecom_adapter = wecom_adapter
        self.storage_adapter = storage_adapter
        self.mq_adapter = mq_adapter

    async def process_webhook_payload(self, xml_payload: str) -> None:
        try:
            data = xmltodict.parse(xml_payload)
            if "xml" in data:
                data = data["xml"]

            msg_type = data.get("MsgType")
            msg_id = data.get("MsgId")
            user_id = data.get("FromUserName")

            logger.info(f"Processing message {msg_id} of type {msg_type} from {user_id}")

            if msg_type == "text":
                await self._handle_text(data)
            elif msg_type == "image":
                await self._handle_image(data)
            elif msg_type == "file":
                await self._handle_file(data)
            else:
                logger.warning(f"Unsupported message type: {msg_type}")

        except Exception as e:
            logger.error(f"Error processing webhook payload: {e}")
            raise

    async def _handle_text(self, data: Dict[str, Any]) -> None:
        content = data.get("Content")
        user_id = data.get("FromUserName")
        msg_id = data.get("MsgId")

        message_data = {
            "msg_id": msg_id,
            "user_id": user_id,
            "type": "text",
            "content": content,
            "timestamp": data.get("CreateTime")
        }
        await self._publish_to_mq(message_data)

    async def _handle_image(self, data: Dict[str, Any]) -> None:
        media_id = data.get("MediaId")
        if not media_id:
            logger.error("MediaId missing in image message")
            return

        user_id = data.get("FromUserName")
        msg_id = data.get("MsgId")

        # AC-3: Download and store
        file_content = await self.wecom_adapter.download_media(media_id)
        file_name = f"{media_id}.jpg"
        storage_path = await self.storage_adapter.upload_file(file_name, io.BytesIO(file_content))

        message_data = {
            "msg_id": msg_id,
            "user_id": user_id,
            "type": "image",
            "media_id": media_id,
            "storage_path": storage_path,
            "timestamp": data.get("CreateTime")
        }
        await self._publish_to_mq(message_data)

    async def _handle_file(self, data: Dict[str, Any]) -> None:
        media_id = data.get("MediaId")
        if not media_id:
            logger.error("MediaId missing in file message")
            return

        file_name = str(data.get("FileName", f"{media_id}"))
        user_id = data.get("FromUserName")
        msg_id = data.get("MsgId")

        # AC-3: Download and store
        file_content = await self.wecom_adapter.download_media(media_id)
        storage_path = await self.storage_adapter.upload_file(file_name, io.BytesIO(file_content))

        message_data = {
            "msg_id": msg_id,
            "user_id": user_id,
            "type": "file",
            "file_name": file_name,
            "media_id": media_id,
            "storage_path": storage_path,
            "timestamp": data.get("CreateTime")
        }
        await self._publish_to_mq(message_data)

    async def _publish_to_mq(self, message_data: Dict[str, Any]) -> None:
        # AC-4: Publish to quotation.parse
        await self.mq_adapter.publish("quotation.parse", message_data)
        logger.info(f"Published message {message_data['msg_id']} to MQ topic quotation.parse")

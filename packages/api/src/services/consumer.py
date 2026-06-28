import json
import asyncio
import aio_pika
import os
import logging
from typing import Any, Dict, List, Tuple, Optional
from src.services.matching.engine import MatchingEngine
from src.services.draft.service import DraftService
from src.services.notification.service import WeComNotificationService
from src.services.file_storage import FileStorageAdapter
from src.db.session import async_session_factory
from packages.shared.types.quotation import QuotationDraft, MaterialMatch, DraftStatus
from src.ai.parser import parse_quotation_request, convert_to_quotation_draft
from datetime import datetime, timezone
import uuid

logger = logging.getLogger(__name__)

class QuotationConsumer:
    def __init__(
        self,
        matching_engine: MatchingEngine,
        notification_service: WeComNotificationService,
        storage_adapter: Optional[FileStorageAdapter] = None
    ):
        self.matching_engine = matching_engine
        self.notification_service = notification_service
        self.storage_adapter = storage_adapter

    async def process_message(self, message_body: bytes) -> None:
        """Process a message from the quotation.parse queue."""
        try:
            data = json.loads(message_body)
            msg_id = data.get("message_id") or data.get("data", {}).get("MsgId") or str(uuid.uuid4())

            email_content = ""
            chat_text = ""
            attachments: List[Tuple[bytes, str]] = []

            # 0. Identify source and extract raw data
            if "sender" in data:  # Mail source
                email_content = data.get("body_text", "")
                if self.storage_adapter:
                    for url in data.get("attachments", []):
                        try:
                            content = await self.storage_adapter.download_file(url)
                            filename = url.split("/")[-1]
                            attachments.append((content, filename))
                        except Exception as e:
                            logger.error(f"Failed to download attachment {url}: {e}")

            elif "type" in data and "data" in data:  # WeCom source
                msg_type = data.get("type")
                msg_data = data.get("data", {})
                if msg_type == "text":
                    chat_text = msg_data.get("Content", "")
                elif msg_type == "file":
                    filename = msg_data.get("FileName", "unknown")
                    # WeCom files are saved locally in storage/wecom/
                    filepath = os.path.join("storage/wecom", filename)
                    if os.path.exists(filepath):
                        with open(filepath, "rb") as f:
                            attachments.append((f.read(), filename))
                elif msg_type == "image":
                    media_id = msg_data.get("MediaId", "unknown")
                    filepath = os.path.join("storage/wecom", f"image_{media_id}")
                    if os.path.exists(filepath):
                        with open(filepath, "rb") as f:
                            attachments.append((f.read(), f"image_{media_id}"))

            # 1. AI Parsing
            logger.info(f"Starting AI parsing for message {msg_id}")
            extracted = await parse_quotation_request(
                email_content=email_content or chat_text,
                attachments=attachments
            )
            initial_draft = convert_to_quotation_draft(extracted, msg_id)
            parsed_quotation = initial_draft.parsed_data

            # 2. Match Customer
            customer_id, customer_score, customer_candidates = self.matching_engine.match_customer(
                parsed_quotation.customer_name or ""
            )

            # 3. Match Materials
            material_matches = []
            all_materials_matched = True
            for item in parsed_quotation.items:
                mat_id, mat_score, mat_candidates = self.matching_engine.match_material(
                    item.code or item.name or ""
                )
                material_matches.append(MaterialMatch(
                    material_id=mat_id,
                    score=mat_score,
                    candidates=mat_candidates
                ))
                if mat_score < 0.85:
                    all_materials_matched = False

            # 4. Create Draft
            needs_confirmation = (customer_score < 0.85) or (not all_materials_matched)

            draft_data = QuotationDraft(
                id=msg_id,
                customer_id=customer_id,
                customer_match_score=customer_score,
                customer_candidates=customer_candidates,
                parsed_data=parsed_quotation,
                material_matches=material_matches,
                status=DraftStatus.DRAFT,
                needs_confirmation=needs_confirmation,
                created_at=datetime.now(timezone.utc),
                updated_at=datetime.now(timezone.utc)
            )

            async with async_session_factory() as session:
                draft_service = DraftService(session)
                await draft_service.create_draft(draft_data)

            # 5. Trigger Notification
            await self.notification_service.send_draft_notification(
                draft_id=msg_id,
                customer_name=parsed_quotation.customer_name or "Unknown Customer",
                status="needs_confirmation" if needs_confirmation else "auto_matched"
            )

        except Exception as e:
            logger.exception(f"Error processing message: {e}")
            # Re-raise so aio-pika can handle retries or dead lettering
            raise

async def start_consumer(
    rabbitmq_url: str,
    matching_engine: MatchingEngine,
    notification_service: WeComNotificationService,
    storage_adapter: Optional[FileStorageAdapter] = None
) -> None:
    """Start the MQ consumer and listen for messages."""
    consumer = QuotationConsumer(matching_engine, notification_service, storage_adapter)

    connection = await aio_pika.connect_robust(rabbitmq_url)
    async with connection:
        channel = await connection.channel()
        # Ensure we don't process more than 10 messages at once
        await channel.set_qos(prefetch_count=10)

        queue = await channel.declare_queue("quotation.parse", durable=True)

        print("MQ Consumer started, listening on 'quotation.parse'...")

        async with queue.iterator() as queue_iter:
            async for message in queue_iter:
                async with message.process():
                    await consumer.process_message(message.body)

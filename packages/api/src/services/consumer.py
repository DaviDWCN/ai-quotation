import json
import asyncio
import aio_pika
import logging
import io
import boto3
from typing import Any, Dict, List, Tuple, Optional
from src.services.matching.engine import MatchingEngine
from src.services.draft.service import DraftService
from src.services.notification.service import WeComNotificationService
from src.db.session import async_session_factory
from packages.shared.types.quotation import QuotationDraft, ParsedQuotation, MaterialMatch, DraftStatus
from src.ai.parser import parse_quotation_request, convert_to_parsed_quotation
from src.config import settings
from datetime import datetime, timezone
import uuid

logger = logging.getLogger(__name__)

class QuotationConsumer:
    def __init__(self, matching_engine: MatchingEngine, notification_service: WeComNotificationService):
        self.matching_engine = matching_engine
        self.notification_service = notification_service

    async def _download_attachments(self, urls: List[str]) -> List[Tuple[bytes, str]]:
        """Download attachments from S3/MinIO."""
        attachments = []
        s3_client = boto3.client(
            "s3",
            endpoint_url=settings.s3_endpoint,
            aws_access_key_id=settings.s3_access_key,
            aws_secret_access_key=settings.s3_secret_key,
            region_name=settings.s3_region,
        )

        for url in urls:
            if not url.startswith(f"s3://{settings.s3_bucket}/"):
                continue

            key = url.replace(f"s3://{settings.s3_bucket}/", "")
            filename = key.split("_", 1)[-1] if "_" in key else key

            try:
                response = await asyncio.to_thread(
                    s3_client.get_object,
                    Bucket=settings.s3_bucket,
                    Key=key
                )
                content = await asyncio.to_thread(response["Body"].read)
                attachments.append((content, filename))
            except Exception as e:
                logger.error(f"Failed to download attachment {url}: {e}")
                # We continue even if one attachment fails, or should we fail the whole message?
                # For now, let's continue to allow AI to parse what it has.

        return attachments

    async def process_message(self, message_body: bytes) -> None:
        """Process a message from the quotation.parse queue."""
        try:
            data = json.loads(message_body)

            # Detect if it's a raw message that needs AI parsing
            is_raw = "body_text" in data or "chat_text" in data or "attachments" in data

            if is_raw:
                logger.info("Processing raw message with AI parser")
                email_content = data.get("body_text") or data.get("chat_text") or ""
                attachment_urls = data.get("attachments", [])

                attachments = await self._download_attachments(attachment_urls)

                extracted = await parse_quotation_request(email_content, attachments)
                parsed_quotation = convert_to_parsed_quotation(extracted)
            else:
                parsed_quotation = ParsedQuotation(**data)

            # 1. Match Customer
            customer_id, customer_score, customer_candidates = self.matching_engine.match_customer(
                parsed_quotation.customer_name or ""
            )

            # 2. Match Materials
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

            # 3. Create Draft
            needs_confirmation = (customer_score < 0.85) or (not all_materials_matched)

            draft_id = str(uuid.uuid4())
            draft_data = QuotationDraft(
                id=draft_id,
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

            # 4. Trigger Notification
            await self.notification_service.send_draft_notification(
                draft_id=draft_id,
                customer_name=parsed_quotation.customer_name or "Unknown Customer",
                status="needs_confirmation" if needs_confirmation else "auto_matched"
            )

        except Exception as e:
            logger.error(f"Error processing message: {e}", exc_info=True)
            # Re-raise to allow MQ retry or dead letter queueing
            raise

async def start_consumer(rabbitmq_url: str, matching_engine: MatchingEngine, notification_service: WeComNotificationService) -> None:
    """Start the MQ consumer and listen for messages."""
    consumer = QuotationConsumer(matching_engine, notification_service)

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

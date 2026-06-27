import json
import asyncio
import aio_pika
from typing import Any, Dict
from src.services.matching.engine import MatchingEngine
from src.services.draft.service import DraftService
from src.services.notification.service import WeComNotificationService
from src.db.session import async_session_factory
from packages.shared.types.quotation import QuotationDraft, ParsedQuotation, MaterialMatch, DraftStatus
from datetime import datetime
import uuid

class QuotationConsumer:
    def __init__(self, matching_engine: MatchingEngine, notification_service: WeComNotificationService):
        self.matching_engine = matching_engine
        self.notification_service = notification_service

    async def process_message(self, message_body: bytes) -> None:
        """Process a message from the quotation.parse queue."""
        try:
            data = json.loads(message_body)
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
                created_at=datetime.utcnow(),
                updated_at=datetime.utcnow()
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
            print(f"Error processing message: {e}")
            # In a real system, we might move this to a dead letter queue
            raise

async def start_consumer(rabbitmq_url: str, matching_engine: MatchingEngine, notification_service: WeComNotificationService):
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

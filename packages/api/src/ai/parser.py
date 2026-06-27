import json
import os
import logging
from typing import Optional, List, cast
from datetime import datetime, timezone
import litellm
from .document_extractor import DocumentExtractor
from .prompts import SYSTEM_PROMPT, USER_PROMPT_TEMPLATE
from .schemas import ExtractedQuotation
from packages.shared.types.quotation import QuotationDraft, QuotationItem

logger = logging.getLogger(__name__)

class AIQuotationParser:
    def __init__(self, model: str = "deepseek/deepseek-chat", temperature: float = 0.2):
        self.model = model
        self.temperature = temperature
        self.extractor = DocumentExtractor()

    async def parse_quotation_request(
        self, email_content: str, attachment_paths: List[str], chat_text: str = ""
    ) -> QuotationDraft:
        attachments_text = ""
        for path in attachment_paths:
            attachments_text += f"--- Attachment: {os.path.basename(path)} ---\n"
            attachments_text += self.extractor.extract_text(path) + "\n"

        user_prompt = USER_PROMPT_TEMPLATE.format(
            email_content=email_content,
            attachments_content=attachments_text,
            chat_text=chat_text
        )

        response_text = await self._call_llm_with_retry(user_prompt)
        extracted_data = self._parse_json(response_text)

        return self._map_to_quotation_draft(extracted_data)

    async def _call_llm_with_retry(self, user_prompt: str) -> str:
        """Calls LLM and retries once if JSON is invalid."""
        response_text = await self._call_llm(user_prompt)

        try:
            json.loads(response_text)
            return response_text
        except json.JSONDecodeError:
            logger.warning("Invalid JSON from LLM, retrying once...")
            return await self._call_llm(user_prompt)

    async def _call_llm(self, user_prompt: str) -> str:
        try:
            response = await litellm.acompletion(
                model=self.model,
                messages=[
                    {"role": "system", "content": SYSTEM_PROMPT},
                    {"role": "user", "content": user_prompt}
                ],
                temperature=self.temperature,
                response_format={"type": "json_object"}
            )
            content = response.choices[0].message.content
            return cast(str, content) if content is not None else "{}"
        except Exception as e:
            logger.error(f"Error calling LLM: {e}")
            return "{}"

    def _parse_json(self, text: str) -> ExtractedQuotation:
        try:
            data = json.loads(text)
            return ExtractedQuotation(**data)
        except Exception as e:
            logger.error(f"JSON parsing error: {e}. Text: {text}")
            return ExtractedQuotation(
                customer_name=None,
                segmentation=None,
                items=[],
                delivery_date=None,
                remarks=None,
                confidence_scores={}
            )

    def _map_to_quotation_draft(self, extracted: ExtractedQuotation) -> QuotationDraft:
        items = []
        for item in extracted.items:
            items.append(QuotationItem(
                material_code=item.material_code,
                quantity=item.quantity,
                unit=item.unit,
                target_price=item.target_price,
                confidence=item.confidence,
                missing=item.missing
            ))

        return QuotationDraft(
            id=None,
            customer_id=None,
            customer_name=extracted.customer_name,
            segmentation=extracted.segmentation,
            items=items,
            delivery_date=extracted.delivery_date,
            remarks=extracted.remarks,
            status="DRAFT",
            created_at=datetime.now(timezone.utc),
            updated_at=datetime.now(timezone.utc),
            confidence_scores=extracted.confidence_scores,
            material_ids=[]
        )

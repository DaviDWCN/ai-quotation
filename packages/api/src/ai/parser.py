import json
import logging
import uuid
from typing import Optional, Any
import litellm
from pydantic import ValidationError

from .schemas import AIParserOutput
from .prompts import SYSTEM_PROMPT, USER_PROMPT_TEMPLATE
from .document_extractor import extract_text
from .confidence import get_overall_confidence
from packages.shared.types.quotation import QuotationDraft, QuotationItem

logger = logging.getLogger(__name__)

async def parse_quotation_request(
    file_path: Optional[str] = None,
    chat_text: Optional[str] = None,
    model: str = "deepseek/deepseek-chat", # Default model
    temperature: float = 0.2,
    max_retries: int = 1
) -> QuotationDraft:
    """
    Parses a quotation request from an email/file and/or chat text using LLM.
    """
    document_content = ""
    if file_path:
        document_content = extract_text(file_path)

    user_prompt = USER_PROMPT_TEMPLATE.format(
        chat_text=chat_text or "No chat context provided.",
        document_content=document_content or "No document content provided."
    )

    messages = [
        {"role": "system", "content": SYSTEM_PROMPT},
        {"role": "user", "content": user_prompt}
    ]

    attempts = 0
    last_exception = None

    while attempts <= max_retries:
        content = ""
        try:
            response = await litellm.acompletion(
                model=model,
                messages=messages,
                temperature=temperature,
                response_format={"type": "json_object"}
            )

            content = response.choices[0].message.content or ""
            if not content:
                raise ValueError("Empty response from LLM")

            data = json.loads(content)
            parsed_output = AIParserOutput.model_validate(data)

            # Convert AIParserOutput to QuotationDraft
            return _map_to_quotation_draft(parsed_output)

        except (ValidationError, json.JSONDecodeError, Exception) as e:
            attempts += 1
            last_exception = e
            logger.warning(f"Attempt {attempts} failed: {e}")
            if attempts <= max_retries:
                # Optional: could add the error message to the next prompt to help LLM correct it
                messages.append({"role": "assistant", "content": content})
                messages.append({"role": "user", "content": f"The previous output had an error: {e}. Please try again and ensure valid JSON conforming to the schema."})

    raise last_exception or ValueError("Failed to parse quotation request")

def _map_to_quotation_draft(output: AIParserOutput) -> QuotationDraft:
    items = []
    for item in output.items:
        items.append(QuotationItem(
            material_code=item.material_code.value,
            quantity=item.quantity.value,
            unit=item.unit.value,
            target_price=item.target_price.value,
            confidence=item.material_code.confidence.value,
            missing=item.material_code.missing
        ))

    overall_confidence = get_overall_confidence(output)

    return QuotationDraft(
        id=str(uuid.uuid4()),
        customer_name=output.customer_name.value,
        segmentation=output.segmentation.value,
        items=items,
        delivery_date=output.delivery_date.value,
        remarks=output.remarks.value,
        confidence=overall_confidence.value,
        status="DRAFT"
    )

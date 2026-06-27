import json
import logging
from typing import List, Optional, Tuple, Any, cast
from litellm import acompletion
from pydantic import ValidationError

from src.ai.schemas import ExtractedQuotation
from src.ai.prompts import QUOTATION_EXTRACTION_SYSTEM_PROMPT, USER_PROMPT_TEMPLATE
from src.ai.document_extractor import extract_documents_text

# Use a workaround for the 'types' name conflict with standard library
import sys
import os
import importlib.util

shared_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../../shared"))

def load_shared_quotation_types() -> Any:
    module_name = "shared_quotation_types"
    file_path = os.path.join(shared_path, "types/quotation.py")
    spec = importlib.util.spec_from_file_location(module_name, file_path)
    if spec and spec.loader:
        module = importlib.util.module_from_spec(spec)
        sys.modules[module_name] = module
        spec.loader.exec_module(module)
        return module
    raise ImportError("Could not load shared quotation types")

try:
    shared_models = load_shared_quotation_types()
    # We use Any for these because they are dynamically loaded and mypy can't track them well
    QuotationDraft: Any = shared_models.QuotationDraft
    QuotationItem: Any = shared_models.QuotationItem
except (ImportError, AttributeError):
    QuotationDraft = None
    QuotationItem = None

logger = logging.getLogger(__name__)

async def parse_quotation_request(
    email_content: str,
    attachments: List[Tuple[bytes, str]],
    model: str = "deepseek/deepseek-chat",
    temperature: float = 0.2
) -> ExtractedQuotation:
    """
    Parses a quotation request from email content and attachments using LLM.
    """
    attachments_text = extract_documents_text(attachments)

    user_prompt = USER_PROMPT_TEMPLATE.format(
        email_content=email_content,
        attachments_content=attachments_text
    )

    messages = [
        {"role": "system", "content": QUOTATION_EXTRACTION_SYSTEM_PROMPT},
        {"role": "user", "content": user_prompt}
    ]

    max_retries = 2
    for attempt in range(max_retries):
        try:
            response = await acompletion(
                model=model,
                messages=messages,
                temperature=temperature,
                # mypy: ignore
                response_format={"type": "json_object"}
            )

            content = response.choices[0].message.content
            if not content:
                raise ValueError("Empty response from LLM")

            data = json.loads(content)
            result = ExtractedQuotation.model_validate(data)
            return cast(ExtractedQuotation, result)

        except (ValidationError, json.JSONDecodeError, ValueError) as e:
            logger.warning(f"Attempt {attempt + 1} failed: {str(e)}")
            if attempt == max_retries - 1:
                raise
            # On retry, we could potentially adjust the prompt, but here we just try again
            continue
        except Exception as e:
            logger.error(f"Unexpected error during LLM call: {str(e)}")
            raise

    raise ValueError("Failed to parse quotation request after retries")

def convert_to_quotation_draft(extracted: ExtractedQuotation, draft_id: str) -> Any:
    """
    Converts ExtractedQuotation to the shared QuotationDraft model.
    Internal IDs (customer_id, material_ids) are not populated here.
    """
    if QuotationItem is None or QuotationDraft is None:
        raise ImportError("Shared quotation models are not available")

    items = []
    for item in extracted.items:
        items.append(QuotationItem(
            material_code=item.material_code.value,
            quantity=item.quantity.value,
            target_price=item.target_price.value,
            unit=item.unit.value,
            remarks=item.remarks.value
        ))

    return QuotationDraft(
        id=draft_id,
        customer_name=extracted.customer_name.value,
        segmentation=extracted.segmentation.value,
        items=items,
        delivery_date=extracted.delivery_date.value,
        remarks=extracted.remarks.value
    )

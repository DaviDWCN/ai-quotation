from typing import Any, Dict

from src.services.wecom.adapter import WeComAdapter


async def send_approval_card(
    adapter: WeComAdapter, user_id: str, draft_id: str, customer_name: str, material_summary: str
) -> Dict[str, Any]:
    """
    Send an approval card message to a WeCom user.
    """
    # Template based on WeCom template_card documentation
    card_content = {
        "msgtype": "template_card",
        "template_card": {
            "card_type": "text_notice",
            "source": {"icon_url": "", "desc": "AI Quotation System"},
            "main_title": {"title": "Quotation Approval Needed"},
            "emphasis_content": {"title": draft_id, "desc": "Draft ID"},
            "quote_area": {
                "type": 1,
                "title": "Details",
                "quote_text": f"Customer: {customer_name}\nMaterials: {material_summary}",
            },
            "horizontal_content_list": [
                {"keyname": "Draft ID", "value": draft_id},
                {"keyname": "Customer", "value": customer_name},
            ],
            "jump_list": [
                {
                    "type": 1,
                    "url": f"https://quotation.example.com/drafts/{draft_id}",
                    "title": "View Draft",
                }
            ],
            "card_action": {
                "type": 1,
                "url": f"https://quotation.example.com/drafts/{draft_id}",
            },
        },
    }

    return await adapter.send_message(user_id, card_content)

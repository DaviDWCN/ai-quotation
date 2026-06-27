import logging
from typing import Any, Dict
from .adapter import WeComAdapter

logger = logging.getLogger(__name__)

class CardPushService:
    def __init__(self, wecom_adapter: WeComAdapter):
        self.wecom_adapter = wecom_adapter

    async def send_approval_card(self, user_id: str, draft_id: str, customer_name: str, material_summary: str) -> None:
        """
        AC-5: Push approval card message
        Template needs to include: Draft ID, Customer Name, Material Summary, and Jump URL.
        """
        # In a real scenario, base_url would come from config
        jump_url = f"https://quotation-system.example.com/drafts/{draft_id}"

        card_data: Dict[str, Any] = {
            "template_id": "approval_card_v1",
            "task_id": f"task_{draft_id}",
            "main_title": {
                "title": "询价单待审批",
                "desc": f"草稿单号: {draft_id}"
            },
            "horizontal_content_list": [
                {
                    "keyname": "客户名称",
                    "value": customer_name
                },
                {
                    "keyname": "物料摘要",
                    "value": material_summary
                }
            ],
            "jump_list": [
                {
                    "type": 1,
                    "url": jump_url,
                    "title": "去审批"
                }
            ],
            "card_action": {
                "type": 1,
                "url": jump_url
            }
        }

        try:
            await self.wecom_adapter.send_template_card(user_id, card_data)
            logger.info(f"Sent approval card for draft {draft_id} to user {user_id}")
        except Exception as e:
            logger.error(f"Failed to send approval card: {e}")
            raise

from .adapter import WeComAdapter

async def send_approval_card(
    adapter: WeComAdapter,
    user_id: str,
    draft_id: str,
    customer_name: str,
    material_summary: str,
    base_url: str = "http://localhost:3000"
) -> None:
    jump_url = f"{base_url}/quotation/draft/{draft_id}"
    await adapter.send_approval_card(
        user_id=user_id,
        draft_id=draft_id,
        customer_name=customer_name,
        material_summary=material_summary,
        jump_url=jump_url
    )

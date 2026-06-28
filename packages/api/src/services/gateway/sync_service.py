import asyncio
import structlog
from typing import List
from src.services.gateway.client import GatewayClient

logger = structlog.get_logger(__name__)

class SyncService:
    def __init__(self, client: GatewayClient) -> None:
        self.client = client

    async def sync_quotation_statuses(self, quotation_ids: List[str]) -> None:
        """
        Periodically pull status of quotations from the legacy system
        and update local records (simulated).
        """
        logger.info("starting_status_sync", count=len(quotation_ids))

        tasks = [self._sync_one(qid) for qid in quotation_ids]
        await asyncio.gather(*tasks, return_exceptions=True)

        logger.info("status_sync_completed")

    async def _sync_one(self, quotation_id: str) -> None:
        try:
            status_update = await self.client.get_status(quotation_id)
            # In a real app, we would update the DB here.
            logger.info(
                "quotation_status_synced",
                quotation_id=quotation_id,
                status=status_update.status
            )
        except Exception as e:
            logger.error(
                "quotation_status_sync_failed",
                quotation_id=quotation_id,
                error=str(e)
            )

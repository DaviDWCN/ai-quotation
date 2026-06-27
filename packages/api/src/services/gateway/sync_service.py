import structlog
from typing import List
from src.services.gateway.client import GatewayClient

logger = structlog.get_logger(__name__)


class GatewaySyncService:
    def __init__(self, gateway_client: GatewayClient) -> None:
        self.gateway_client = gateway_client

    async def sync_quotation_statuses(self, external_ids: List[str]) -> None:
        """
        Synchronizes local quotation statuses with the legacy system.
        In a real implementation, this would update the local database.
        """
        for external_id in external_ids:
            try:
                info = await self.gateway_client.get_status(external_id)
                logger.info(
                    "Synced quotation status",
                    external_id=external_id,
                    status=info.status,
                )
                # TODO: Update local database status here
            except Exception as e:
                logger.error(
                    "Failed to sync quotation status",
                    external_id=external_id,
                    error=str(e),
                )

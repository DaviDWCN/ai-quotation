import asyncio
import structlog
from typing import List, Optional
from .client import gateway
from .schemas import LegacyQuotationResponse, LegacyQuotationStatus

logger = structlog.get_logger(__name__)

class StatusSyncService:
    def __init__(self) -> None:
        self.gateway = gateway
        self._stop_event = asyncio.Event()
        self._is_running = False

    async def sync_all_pending(self) -> List[LegacyQuotationResponse]:
        """
        Pull all SUBMITTED quotations from the legacy system and update local status.
        """
        logger.info("status_sync_start", status_to_sync="SUBMITTED")

        try:
            submitted_quotations = await self.gateway.list_quotations(
                status=LegacyQuotationStatus.SUBMITTED
            )

            for quotation in submitted_quotations:
                # Mocking the sync process
                logger.info(
                    "status_sync_item",
                    quotation_id=quotation.id,
                    new_status=quotation.status
                )

            logger.info(
                "status_sync_complete",
                count=len(submitted_quotations)
            )
            return submitted_quotations

        except Exception as e:
            logger.error("status_sync_failed", error=str(e))
            raise

    async def start_periodic_sync(self, interval_seconds: int = 60) -> None:
        """
        Starts the periodic synchronization loop.
        """
        if self._is_running:
            logger.warning("status_sync_loop_already_running")
            return

        self._is_running = True
        self._stop_event.clear()
        logger.info("status_sync_loop_starting", interval=interval_seconds)

        while not self._stop_event.is_set():
            try:
                await self.sync_all_pending()
            except Exception as e:
                logger.error("status_sync_loop_error", error=str(e))

            try:
                # Wait for interval or stop event
                await asyncio.wait_for(self._stop_event.wait(), timeout=interval_seconds)
            except asyncio.TimeoutError:
                # Normal timeout, continue loop
                pass

        self._is_running = False
        logger.info("status_sync_loop_stopped")

    def stop_periodic_sync(self) -> None:
        logger.info("status_sync_loop_stopping_signal")
        self._stop_event.set()

sync_service = StatusSyncService()

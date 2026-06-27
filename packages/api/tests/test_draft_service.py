import pytest
import pytest_asyncio
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
from src.db.models import Base
from src.services.draft.service import DraftService
from packages.shared.types.quotation import QuotationDraft, ParsedQuotation, DraftStatus
import uuid
from datetime import datetime

# Use in-memory SQLite for testing
DATABASE_URL = "sqlite+aiosqlite:///:memory:"

@pytest_asyncio.fixture
async def db_session():
    engine = create_async_engine(DATABASE_URL)
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    Session = async_sessionmaker(engine, expire_on_commit=False)
    async with Session() as session:
        yield session

    await engine.dispose()

@pytest.mark.asyncio
async def test_create_and_get_draft(db_session):
    service = DraftService(db_session)

    draft_id = str(uuid.uuid4())
    parsed_data = ParsedQuotation(
        customer_name="Test Customer",
        items=[],
        confidence=0.9
    )

    draft_data = QuotationDraft(
        id=draft_id,
        parsed_data=parsed_data,
        status="draft"
    )

    created = await service.create_draft(draft_data)
    assert created.id == draft_id

    fetched = await service.get_draft(draft_id)
    assert fetched is not None
    assert fetched.id == draft_id
    assert fetched.parsed_data["customer_name"] == "Test Customer"

@pytest.mark.asyncio
async def test_update_draft(db_session):
    service = DraftService(db_session)
    draft_id = str(uuid.uuid4())
    draft_data = QuotationDraft(
        id=draft_id,
        parsed_data=ParsedQuotation(customer_name="Initial"),
        status="draft"
    )
    await service.create_draft(draft_data)

    updated = await service.update_draft(draft_id, {"status": DraftStatus.CONFIRMED})
    assert updated.status == DraftStatus.CONFIRMED

    fetched = await service.get_draft(draft_id)
    assert fetched.status == DraftStatus.CONFIRMED

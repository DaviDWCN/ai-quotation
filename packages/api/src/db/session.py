from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from src.config import settings

# In a real app, this would come from settings.
# For now, using a placeholder or default.
DATABASE_URL = getattr(settings, "database_url", "postgresql+asyncpg://postgres:postgres@localhost:5432/postgres")

engine = create_async_engine(DATABASE_URL, echo=True)
async_session_factory = async_sessionmaker(engine, expire_on_commit=False)

async def get_db():
    async with async_session_factory() as session:
        yield session

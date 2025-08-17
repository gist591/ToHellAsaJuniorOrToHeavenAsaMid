from collections.abc import AsyncIterator
from contextlib import asynccontextmanager

from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine

from to_the_hell.oncallhub.core.config import settings

async_engine = create_async_engine(url=settings.DATABASE_URL_asyncpg)

async_session_factory = async_sessionmaker(async_engine, expire_on_commit=False)

@asynccontextmanager
async def get_session() -> AsyncIterator[AsyncSession]:
    async with async_session_factory() as session:
        yield session

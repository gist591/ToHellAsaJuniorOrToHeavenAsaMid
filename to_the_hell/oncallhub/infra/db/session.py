from contextlib import asynccontextmanager
from typing import AsyncIterator
from sqlalchemy import create_async_engine, mapped_column, Mapped, async_sessionmaker
from sqlalchemy.ext.asyncio import AsyncSession
from core.config import settings


async_engine = create_async_engine(url=settings.DATABASE_URL_asyncpg)

async_session_factory = async_sessionmaker(async_engine, expire_on_commit=False)

@asynccontextmanager
async def get_session() -> AsyncIterator[AsyncSession]:
    async with async_session_factory as session:
        yield session

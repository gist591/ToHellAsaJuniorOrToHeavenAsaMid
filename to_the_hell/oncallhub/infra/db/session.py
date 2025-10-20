from collections.abc import AsyncGenerator
from contextlib import asynccontextmanager

from sqlalchemy.ext.asyncio import (
    AsyncEngine,
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)

from to_the_hell.oncallhub.core.config import settings
from to_the_hell.oncallhub.infra.db.models.base import Base

async_engine: AsyncEngine = create_async_engine(url=settings.get_database_url)
async_session_factory = async_sessionmaker(async_engine, expire_on_commit=False)


async def init_db() -> None:
    """Initialize database tables"""
    async with async_engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


async def drop_db() -> None:
    """Drop all database tables"""
    async with async_engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)


@asynccontextmanager
async def get_session() -> AsyncGenerator[AsyncSession]:
    """Get async database session"""
    async with async_session_factory() as session:
        try:
            yield session
            await session.commit()
        except Exception:
            await session.rollback()
            raise
        finally:
            await session.close()

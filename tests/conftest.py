pytest_plugins = ["pytest_asyncio"]

from collections.abc import AsyncIterator

import pytest_asyncio
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine

from to_the_hell.oncallhub.domain.entities import Devops
from to_the_hell.oncallhub.domain.repositories import BaseDevopsRepository


class FakeDevopsRepostitory(BaseDevopsRepository):
    """
    Fake devops repository for tests
    """

    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def create(self, devops: Devops) -> Devops:
        return devops


FAKE_DATABASE_URL = "sqlite+aiosqlite:///:memory:"

async_engine = create_async_engine(url=FAKE_DATABASE_URL)
async_session_factory = async_sessionmaker(async_engine, expire_on_commit=False)


@pytest_asyncio.fixture  # type: ignore[misc]
async def get_session() -> AsyncIterator[AsyncSession]:
    async_engine = create_async_engine(url=FAKE_DATABASE_URL, echo=True)
    async_session_factory = async_sessionmaker(async_engine, expire_on_commit=False)

    async with async_session_factory() as session:
        yield session

    await async_engine.dispose()

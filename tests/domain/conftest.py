from uuid import UUID

import pytest
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.pool import StaticPool

from to_the_hell.oncallhub.infra.db.models.user import UserORM
from to_the_hell.oncallhub.domain.repositories.base import UserRepository


class FakeUserRepostitory(UserRepository):
    """
    Fuck
    """


@pytest.fixture
async def async_session():
    engine = create_async_engine(
        "sqlite+aiosqlite:///:memory:",
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
    )
    return engine

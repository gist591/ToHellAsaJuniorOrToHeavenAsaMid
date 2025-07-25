import pytest
from uuid import UUID
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.pool import StaticPool

from to_the_hell.oncallhub.infra.db import get_session
from to_the_hell.oncallhub.infra.db.models.user import UserORM


class FakeUserRepostitory():
    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def create(self, user_id: UUID, name: str, telegram_username: str) -> UserORM:
        user = UserORM(user_id, name, telegram_username)

        self.session.add(user)
        await self.session.commit()
        await self.session.refresh(user)
        return user


@pytest.fixture
async def async_session():
    engine = create_async_engine(
        'sqlite+aiosqlite:///:memory:',
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
    )

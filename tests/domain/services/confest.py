import pytest
from sqlalchemy.ext.asyncio.session import AsyncSession

from to_the_hell.oncallhub.infra.db import get_session


class FakeUserRepostitory():
    def __init__(self, session:AsyncSession) -> None:
        self.session = session

    async def create(self, user_id: UUID, name: str, telegram_username: str) -> UserORM:
        user = UserORM(user_id, name, telegram_username)

        self.session.add(user)
        await self.session.commit()
        await self.session.refresh(user)
        return user

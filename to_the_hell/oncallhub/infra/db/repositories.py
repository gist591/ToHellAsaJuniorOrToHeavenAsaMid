from datetime import datetime
from uuid import UUID

from . import DutyORM, UserORM
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession


class PostgresDutyRepository:
    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def create(self, user_id: UUID, start_time: datetime,
        end_time: datetime) -> DutyORM:
        duty = DutyORM(
            user_id=user_id,
            start_time=start_time,
            end_time=end_time,
            status=False
        )

        self.session.add(duty)
        await self.session.commit()
        await self.session.refresh(duty)
        return duty

    async def get_current_duty(self) -> DutyORM:
        stmt = select(DutyORM).where(
            DutyORM.end_time >= datetime.now(),
            datetime.now() >= DutyORM.start_time
        )
        res = await self.session.execute(stmt)
        return res.scalar_one_or_none()


class PostgresUserRepository: # TODO: нарушение DRY с классом FakeUserRepository (tests/domain/services/confest.py)
    def __init__(self, session:AsyncSession) -> None:
        self.session = session

    async def create(self, user_id: UUID, name: str, telegram_username: str) -> UserORM:
        user = UserORM(
            user_id=user_id,
            name=name,
            telegram_username=telegram_username
        )

        self.session.add(user)
        await self.session.commit()
        await self.session.refresh(user)
        return user

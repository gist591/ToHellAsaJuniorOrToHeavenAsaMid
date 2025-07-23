from datetime import datetime
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from api.schemas import User
from infra.db import DutyORM
from uuid import UUID


class DutyRepository:
    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def create(self, user_id: UUID, start_time: datetime,
        end_time: datetime) -> DutyORM:
        duty = DutyORM(user_id, start_time, end_time, False)
        self.session.add(duty)
        await self.session.commit()
        await self.session.refresh(duty)
        return duty

    async def get_current_duty(self) -> DutyORM:
        stmt = select(DutyORM).where(
            DutyORM.end_time >= datetime.now(),
            datetime.now >= DutyORM.start_time
        )
        res = await self.session.execute(stmt)
        return res.scalar_one_or_none()

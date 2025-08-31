from datetime import UTC, datetime

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from to_the_hell.oncallhub.domain.entities import Duty
from to_the_hell.oncallhub.domain.repositories import (
    BaseDutyRepository,
)
from to_the_hell.oncallhub.domain.value_objects import DutyId, TimeRange, UserId

from . import DutyORM


class PostgresDutyRepository(BaseDutyRepository):
    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def create(self, duty: Duty) -> Duty:
        duty_orm = DutyORM()
        duty_orm.user_id = int(str(duty.user_id))
        duty_orm.start_time = duty.time_range.start
        duty_orm.end_time = duty.time_range.end
        duty_orm.status = duty.status

        self.session.add(duty_orm)
        await self.session.commit()
        await self.session.refresh(duty_orm)
        return Duty(
            id=DutyId.from_string(str(duty_orm.id)),
            user_id=UserId.from_string(str(duty_orm.user_id)),
            time_range=TimeRange(duty_orm.start_time, duty_orm.end_time),
            status=duty_orm.status,
        )

    async def get_current_duty(self) -> Duty | None:
        stmt = select(DutyORM).where(
            DutyORM.end_time >= datetime.now(UTC),
            datetime.now(UTC) >= DutyORM.start_time,
            DutyORM.status,
        )
        res = await self.session.execute(stmt)
        duty_orm = res.scalar_one_or_none()

        if not duty_orm:
            return None

        return Duty(
            id=DutyId.from_string(str(duty_orm.id)),
            user_id=UserId.from_string(str(duty_orm.user_id)),
            time_range=TimeRange(duty_orm.start_time, duty_orm.end_time),
            status=duty_orm.status,
        )


class PostgresDevopsRepository(BaseDevopsRepository):
    """Repository for Devops on Postgres"""

    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def create(self, devops: Devops) -> Devops:
        user_orm = DevopsORM()
        devops_orm.name = devops.name
        devops_orm.telegram_username = devops.telegram_username

        self.session.add(devops_orm)
        await self.session.commit()
        await self.session.refresh(devops_orm)
        return Devops(
            id=DevopsId.from_string(str(devops_orm.id)),
            name=devops_orm.name,
            telegram_username=devops_orm.telegram_username,
        )

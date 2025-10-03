from datetime import UTC, datetime
from uuid import UUID

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from to_the_hell.oncallhub.domain.entities import Devops, Duty, Incident
from to_the_hell.oncallhub.domain.repositories import (
    BaseDevopsRepository,
    BaseDutyRepository,
    BaseIncidentRepository,
)
from to_the_hell.oncallhub.infra.db.models import DevopsORM, DutyORM, IncidentORM


class PostgresDutyRepository(BaseDutyRepository):
    """Repository for duty operations in PostgreSQL"""

    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def create(self, duty: Duty) -> Duty:
        """Create new duty in database"""
        duty_orm = DutyORM()
        duty_orm.user_id = duty.devops_id
        duty_orm.start_time = duty.start_time
        duty_orm.end_time = duty.end_time
        duty_orm.status = duty.status

        self.session.add(duty_orm)
        await self.session.commit()
        await self.session.refresh(duty_orm)

        return Duty(
            id=duty_orm.id,
            devops_id=duty.devops_id,
            start_time=duty_orm.start_time,
            end_time=duty_orm.end_time,
            status=duty_orm.status,
            created_at=None,
        )

    async def get_current_duty(self) -> Duty | None:
        """Get current active duty"""
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
            id=duty_orm.id,
            devops_id=duty_orm.user_id,
            start_time=duty_orm.start_time,
            end_time=duty_orm.end_time,
            status=duty_orm.status,
            created_at=None,
        )

    async def get_all_duties(self) -> list[Duty]:
        """Get all duties from database"""
        stmt = select(DutyORM)
        res = await self.session.execute(stmt)
        duties_orm = res.scalars().all()

        return [
            Duty(
                id=duty_orm.id,
                devops_id=duty_orm.user_id,
                start_time=duty_orm.start_time,
                end_time=duty_orm.end_time,
                status=duty_orm.status,
                created_at=None,
            )
            for duty_orm in duties_orm
        ]


class PostgresDevopsRepository(BaseDevopsRepository):
    """Repository for Devops on Postgres"""

    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def create(self, devops: Devops) -> Devops:
        """Create new devops in database"""
        devops_orm = DevopsORM()
        devops_orm.name = devops.name
        devops_orm.telegram_username = devops.email

        self.session.add(devops_orm)
        await self.session.commit()
        await self.session.refresh(devops_orm)

        return Devops(
            id=devops_orm.id,
            name=devops_orm.name,
            email=devops_orm.telegram_username,
            phone=None,
            created_at=None,
        )


class PostgresIncidentRepository(BaseIncidentRepository):
    """Repository for Incidents on Postgres"""

    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def create(self, incident: Incident) -> Incident:
        """Create new incident in database"""
        return incident

    async def get_all_incidents(
        self,
        limit: int | None = None,
        offset: int | None = None,
        status: str | None = None,
        assigned_to: UUID | None = None,
    ) -> list[Incident]:
        query = select(IncidentORM)

        if status:
            query = query.where(IncidentORM.status == status)
        if assigned_to:
            query = query.where(IncidentORM.assigned_duty == assigned_to)

        if limit:
            query = query.limit(limit)
        if offset:
            query = query.offset(offset)

        result = await self.session.execute(query)
        incidents_orm = result.scalars().all()

        return [self._orm_to_entity(orm) for orm in incidents_orm]

    def _orm_to_entity(self, orm: IncidentORM) -> Incident:
        """Convert ORM model to domain entity"""
        return Incident(
            title="",
            description=orm.description,
            priority=orm.priority,
        )

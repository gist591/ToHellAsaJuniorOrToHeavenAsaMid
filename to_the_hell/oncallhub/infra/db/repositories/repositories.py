from datetime import UTC, datetime
from uuid import UUID

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from to_the_hell.oncallhub.domain.entities import Devops, Duty, Incident
from to_the_hell.oncallhub.domain.repositories import (
    BaseDevopsRepository,
    BaseDutyRepository,
    BaseIncidentRepository,
)
from to_the_hell.oncallhub.infra.db.models import (
    DevopsORM,
    DutyORM,
    IncidentDutyORM,
    IncidentORM,
)


class PostgresDutyRepository(BaseDutyRepository):
    """PostgreSQL repository for Duty operations"""

    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def create(self, duty: Duty) -> Duty:
        """Create new duty in database"""
        duty_orm = DutyORM()
        duty_orm.devops_id = duty.devops_id
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
            devops_id=duty_orm.devops_id,
            start_time=duty_orm.start_time,
            end_time=duty_orm.end_time,
            status=duty_orm.status,
        )

    def _orm_to_entity(self, orm: DutyORM) -> Duty:
        """Convert ORM model to domain entity"""
        return Duty(
            id=orm.id,
            devops_id=orm.devops_id,
            start_time=orm.start_time,
            end_time=orm.end_time,
            status=orm.status,
            created_at=orm.created_at,
        )

    async def get_all_duties(self) -> list[Duty]:
        """Get all duties from database"""
        stmt = select(DutyORM)
        res = await self.session.execute(stmt)
        duties_orm = res.scalars().all()

        return [
            Duty(
                id=duty_orm.id,
                devops_id=duty_orm.devops_id,
                start_time=duty_orm.start_time,
                end_time=duty_orm.end_time,
                status=duty_orm.status,
            )
            for duty_orm in duties_orm
        ]


class PostgresDevopsRepository(BaseDevopsRepository):
    """PostgreSQL repository for DevOps users"""

    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def create(self, devops: Devops) -> Devops:
        """Create new devops in database"""
        devops_orm = DevopsORM()
        devops_orm.name = devops.name
        devops_orm.telegram_username = devops.telegram_username
        devops_orm.email = devops.email
        devops_orm.phone = devops.phone

        self.session.add(devops_orm)
        await self.session.commit()
        await self.session.refresh(devops_orm)

        return Devops(
            id=devops_orm.id,
            name=devops_orm.name,
            telegram_username=devops_orm.telegram_username,
            email=devops_orm.email,
            phone=devops_orm.phone,
        )


class PostgresIncidentRepository(BaseIncidentRepository):
    """Repository for Incidents on Postgres"""

    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def create(self, incident: Incident) -> Incident:
        """Create new incident in database"""
        incident_orm = IncidentORM()
        incident_orm.title = incident.title
        incident_orm.description = incident.description
        incident_orm.status = incident.status
        incident_orm.priority = incident.priority
        incident_orm.created_at = incident.created_at
        incident_orm.updated_at = incident.updated_at
        incident_orm.resolved_at = incident.resolved_at
        incident_orm.closed_at = incident.closed_at

        self.session.add(incident_orm)
        await self.session.commit()
        await self.session.refresh(incident_orm)

        return Incident(
            id=incident_orm.id,
            title=incident_orm.title,
            description=incident_orm.description,
            priority=incident_orm.priority,
        )

    async def get_all_incidents(
        self,
        limit: int | None = None,
        offset: int | None = None,
        status: str | None = None,
        assigned_to: UUID | None = None,
    ) -> list[Incident]:
        """Get incidents with filtering"""
        query = select(IncidentORM)

        if status:
            query = query.where(IncidentORM.status == status)
        if assigned_to:
            query = query.where(IncidentORM.incident_duties == assigned_to)

        if limit:
            query = query.limit(limit)
        if offset:
            query = query.offset(offset)

        result = await self.session.execute(query)
        incidents_orm = result.scalars().all()

        return [self._orm_to_entity(orm) for orm in incidents_orm]

    def _orm_to_entity(self, incident_orm: IncidentORM) -> Incident:
        """Convert ORM model to domain entity"""
        return Incident(
            id=incident_orm.id,
            title=incident_orm.title,
            description=incident_orm.description,
            priority=incident_orm.priority,
        )

    async def assign_to_duty(
        self, incident_id: UUID, duty_id: UUID, assigned_by: UUID | None = None
    ) -> None:
        """Assign incident on duty"""
        from ..models.incident_duty import IncidentDutyORM

        assignment = IncidentDutyORM(
            incident_id=incident_id, duty_id=duty_id, assigned_by=assigned_by
        )

        self.session.add(assignment)
        await self.session.commit()

    async def get_incident_with_duties(self, incident_id: UUID) -> IncidentORM | None:
        """Receive an incident with information about scheduled shifts"""
        stmt = (
            select(IncidentORM)
            .options(
                selectinload(IncidentORM.incident_duties).selectinload(
                    IncidentDutyORM.duty
                )
            )
            .where(IncidentORM.id == incident_id)
        )

        result = await self.session.execute(stmt)
        return result.scalar_one_or_none()

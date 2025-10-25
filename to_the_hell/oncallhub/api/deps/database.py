from collections.abc import AsyncIterator
from typing import Annotated

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from to_the_hell.oncallhub.domain.application.dependencies import (
    get_command_bus as create_command_bus,
)
from to_the_hell.oncallhub.domain.commands.base import CommandBus
from to_the_hell.oncallhub.domain.repositories import (
    BaseDevopsRepository,
    BaseDutyRepository,
    BaseIncidentRepository,
)
from to_the_hell.oncallhub.infra.db.repositories import (
    PostgresDevopsRepository,
    PostgresDutyRepository,
    PostgresIncidentRepository,
)
from to_the_hell.oncallhub.infra.db.session import async_session_factory


async def get_session() -> AsyncIterator[AsyncSession]:
    """
    Provide database session for FastAPI request scope
    Each HTTP request gets its own session
    """
    async with async_session_factory() as session:
        try:
            yield session
            await session.commit()
        except Exception:
            await session.rollback()
            raise
        finally:
            await session.close()


SessionDep = Annotated[AsyncSession, Depends(get_session)]


async def get_duty_repository(
    session: SessionDep,
) -> BaseDutyRepository:
    """
    Provide duty repository with injected session

    Creates new repository instance for each request
    with request-scoped session.
    """
    return PostgresDutyRepository(session)


async def get_devops_repository(
    session: SessionDep,
) -> BaseDevopsRepository:
    """Provide devops repository with injected session."""
    return PostgresDevopsRepository(session)


async def get_incident_repository(
    session: SessionDep,
) -> BaseIncidentRepository:
    """Provide incident repository with injected session."""
    return PostgresIncidentRepository(session)


DutyRepoDep = Annotated[BaseDutyRepository, Depends(get_duty_repository)]
DevopsRepoDep = Annotated[BaseDevopsRepository, Depends(get_devops_repository)]
IncidentRepoDep = Annotated[BaseIncidentRepository, Depends(get_incident_repository)]


async def get_command_bus_dependency(
    session: SessionDep,
) -> CommandBus:
    """
    Provide configured Command Bus for FastAPI request
    """
    return await create_command_bus(session)


CommandBusDep = Annotated[CommandBus, Depends(get_command_bus_dependency)]

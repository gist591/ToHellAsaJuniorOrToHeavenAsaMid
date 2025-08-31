from uuid import UUID

from fastapi import APIRouter, Depends
from fastapi.exceptions import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from to_the_hell.oncallhub.api.schemas.incident import IncidentSchema
from to_the_hell.oncallhub.domain.entities import Duty
from to_the_hell.oncallhub.infra.db import get_session
from to_the_hell.oncallhub.infra.db.repositories import PostgresIncidentRepository

router = APIRouter()


@router.get("/incidents")  # type: ignore[misc]
def get_all_incidents(session: AsyncSession = Depends(get_session)) -> list[Duty]:
    """
    Get all incidents in history

    Return:
        404: current duty is not exist
        200: current duty
    """

    repo = PostgresIncidentRepository(session)
    incidents = repo.get_all_incidents()

    if not incidents:
        raise HTTPException(status_code=404, detail="No incidents found")

    incident_schemas = [
        IncidentSchema(
            id=UUID(str(incident.id)),
            description=incident.description,
            incident_created_at=incident.incident_created,
            incident_assigned_at=incident.incident.assigned,
            status=incident.status,
            priority=incident.priority,
            assigned_duty=incident.assigned_duty,
        )
        for incident in incidents
    ]

    return incident_schemas

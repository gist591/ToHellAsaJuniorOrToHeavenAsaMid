from uuid import UUID

from pydantic import BaseModel

from to_the_hell.oncallhub.domain.value_objects.incident_priority import (
    IncidentPriority,
)

from .duty import DutySchema


class IncidentSchema(BaseModel):
    id: UUID
    description: str
    incident_created_at: float
    status: str
    incident_assigned_at: float | None
    priority: IncidentPriority
    assigned_duty: list[DutySchema] | None

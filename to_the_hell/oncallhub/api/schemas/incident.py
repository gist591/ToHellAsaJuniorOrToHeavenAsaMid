from uuid import UUID

from pydantic import BaseModel

from .duty import DutySchema


class IncidentSchema(BaseModel):  # type: ignore[misc]
    id: UUID
    description: str
    incident_created_at: float
    status: str
    incident_assigned_at: float
    priority: int
    assigned_duty: list[DutySchema] | None

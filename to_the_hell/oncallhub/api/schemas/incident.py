from uuid import UUID

from pydantic import BaseModel

from .duty import DutySchema


class IncidentSchema(BaseModel):  # type: ignore[misc]
    id: UUID
    description: str
    created_at: float
    status: bool
    duty: DutySchema | None

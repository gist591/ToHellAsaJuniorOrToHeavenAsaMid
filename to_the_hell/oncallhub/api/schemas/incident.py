from uuid import UUID

from pydantic import BaseModel

from .duty import Duty


class Incident(BaseModel):
    id: UUID
    description: str
    create_start: float
    status: bool
    duty: Duty

from pydantic import BaseModel, Field
from uuid import UUID

from duty import Duty


class Incident(BaseModel):
    id: UUID
    description: str
    create_start: float
    status: bool
    duty: Duty

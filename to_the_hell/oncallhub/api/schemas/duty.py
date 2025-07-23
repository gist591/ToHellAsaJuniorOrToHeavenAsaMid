from pydantic import BaseModel, Field
from uuid import UUID


class Duty(BaseModel):
    id: UUID
    user_id: UUID
    start_time: float
    end_time: float
    status: bool

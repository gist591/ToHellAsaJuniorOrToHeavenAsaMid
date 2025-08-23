from uuid import UUID

from pydantic import BaseModel


class DutySchema(BaseModel):  # type: ignore[misc]
    id: UUID
    user_id: UUID
    start_time: float
    end_time: float
    status: bool

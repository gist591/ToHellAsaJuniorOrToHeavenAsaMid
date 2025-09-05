from datetime import datetime
from uuid import UUID

from pydantic import BaseModel


class DutySchema(BaseModel):  # type: ignore[misc]
    devops_id: UUID
    start_time: datetime
    end_time: datetime
    status: bool
    id: UUID
    created_at: datetime | None = None

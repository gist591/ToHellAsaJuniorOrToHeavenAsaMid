from datetime import datetime

from pydantic import BaseModel


class DutySchema(BaseModel):
    devops_id: int
    start_time: datetime
    end_time: datetime
    status: bool
    id: int
    created_at: datetime | None = None

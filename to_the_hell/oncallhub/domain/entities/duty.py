from dataclasses import dataclass
from datetime import datetime
from uuid import UUID


@dataclass
class Duty:
    devops_id: UUID
    start_time: datetime
    end_time: datetime
    status: bool
    id: UUID | None = None
    created_at: datetime | None = None

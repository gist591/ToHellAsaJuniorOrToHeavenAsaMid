from uuid import UUID

from pydantic import BaseModel

from to_the_hell.oncallhub.domain.value_objects.time_range import TimeRange


class DutySchema(BaseModel):  # type: ignore[misc]
    id: UUID
    user_id: UUID
    time_range: TimeRange
    status: bool

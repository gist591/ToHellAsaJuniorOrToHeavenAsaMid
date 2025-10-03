from dataclasses import dataclass
from datetime import datetime
from uuid import UUID

from to_the_hell.oncallhub.domain.value_objects import TimeRange


@dataclass
class Duty:
    """Domain entity for duty"""

    devops_id: UUID
    start_time: datetime
    end_time: datetime
    status: bool
    id: UUID
    created_at: datetime | None = None

    @property
    def time_range(self) -> TimeRange:
        """Get time range of duty"""
        return TimeRange(start=self.start_time, end=self.end_time)

    @classmethod
    def create_from_time_range(
        cls,
        devops_id: UUID,
        time_range: TimeRange,
        status: bool,
        id: UUID,
        created_at: datetime | None = None,
    ) -> "Duty":
        """Create duty from time range"""
        return cls(
            devops_id=devops_id,
            start_time=time_range.start,
            end_time=time_range.end,
            status=status,
            id=id,
            created_at=created_at,
        )

from dataclasses import dataclass

from to_the_hell.oncallhub.domain.value_objects import DutyId, TimeRange, UserId


@dataclass
class Duty:
    id: DutyId
    user_id: UserId
    time_range: TimeRange
    status: bool

    def is_active(self) -> bool:
        return self.status

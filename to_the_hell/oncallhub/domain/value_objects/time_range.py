from dataclasses import dataclass
from datetime import datetime


@dataclass(frozen=True)
class TimeRange:
    start: datetime
    end: datetime

    def __post_init__(self) -> None:
        if self.start >= self.end:
            raise ValueError(f"Invalid time range: {self.start} >= {self.end}")

    @property
    def duration_hours(self) -> float:
        return (self.end - self.start).total_seconds() / 3600

    def contains(self, timestamp: datetime) -> bool:
        return self.start <= timestamp <= self.end

    def overlaps_with(self, other: "TimeRange") -> bool:
        return not (self.end <= other.start or self.start >= other.end)

    def __str__(self) -> str:
        return f"{self.start.isoformat()} - {self.end.isoformat()}"

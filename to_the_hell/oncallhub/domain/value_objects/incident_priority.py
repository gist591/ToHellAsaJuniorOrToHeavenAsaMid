from enum import Enum
from typing import Any


class IncidentPriority(Enum):
    """Приоритеты инцидентов"""

    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"

    def __lt__(self, other: Any) -> bool:
        if not isinstance(other, IncidentPriority):
            return NotImplemented

        priority_order = {
            IncidentPriority.LOW: 1,
            IncidentPriority.MEDIUM: 2,
            IncidentPriority.HIGH: 3,
            IncidentPriority.CRITICAL: 4,
        }

        return priority_order[self] < priority_order[other]

    def __str__(self) -> str:
        return self.value

    @classmethod
    def from_string(cls, value: str) -> "IncidentPriority":
        """Создать приоритет из строки"""
        try:
            return cls(value.lower())
        except ValueError as e:
            raise ValueError(f"Invalid priority: {value}") from e

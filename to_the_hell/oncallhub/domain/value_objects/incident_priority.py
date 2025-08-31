from enum import Enum


class IncidentPriority(Enum):
    """Приоритеты инцидентов"""

    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"

    def __lt__(self, other):
        if not isinstance(other, IncidentPriority):
            return NotImplemented

        priority_order = {
            IncidentPriority.LOW: 1,
            IncidentPriority.MEDIUM: 2,
            IncidentPriority.HIGH: 3,
            IncidentPriority.CRITICAL: 4,
        }

        return priority_order[self] < priority_order[other]

    def __str__(self):
        return self.value

    @classmethod
    def from_string(cls, value: str) -> "IncidentPriority":
        """Создать приоритет из строки"""
        try:
            return cls(value.lower())
        except ValueError:
            raise ValueError(f"Invalid priority: {value}")

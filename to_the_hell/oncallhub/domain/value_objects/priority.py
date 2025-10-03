from dataclasses import dataclass
from enum import Enum


class PriorityLevel(Enum):
    """Уровни приоритета"""

    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"


@dataclass(frozen=True)
class Priority:
    level: PriorityLevel

    @property
    def multiplier(self) -> float:
        """Вычисляемое свойство"""
        return {
            PriorityLevel.LOW: 1.0,
            PriorityLevel.MEDIUM: 2.5,
            PriorityLevel.HIGH: 5.0,
            PriorityLevel.CRITICAL: 10.0,
        }[self.level]

    def __str__(self) -> str:
        return self.level.value

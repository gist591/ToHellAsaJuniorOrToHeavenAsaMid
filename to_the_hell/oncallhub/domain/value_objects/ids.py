from dataclasses import dataclass
from typing import TypeVar
from uuid import UUID, uuid4

T = TypeVar("T", bound="EntityId")


@dataclass(frozen=True)
class EntityId:
    """Базовый класс для всех ID"""

    value: UUID

    @classmethod
    def generate(cls: type[T]) -> T:
        return cls(value=uuid4())

    @classmethod
    def from_string(cls: type[T], value: str) -> T:
        return cls(value=UUID(value))

    def __str__(self) -> str:
        return str(self.value)


class DevopsId(EntityId):
    """ID of devops"""

    pass


class IncidentId(EntityId):
    """ID of incident"""

    pass


class DutyId(EntityId):
    """ID of duty"""

    pass

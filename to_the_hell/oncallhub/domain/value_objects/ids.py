from dataclasses import dataclass
from typing import TypeVar

T = TypeVar("T", bound="EntityId")


@dataclass(frozen=True)
class EntityId:
    """
    Base class for all entity IDs
    """

    value: int

    @classmethod
    def from_int(cls: type[T], value: int) -> T:
        """Create EntityId from integer value"""
        return cls(value=value)

    def __str__(self) -> str:
        """String representation of ID"""
        return str(self.value)


class DevopsId(EntityId):
    """ID of devops user"""

    pass


class IncidentId(EntityId):
    """ID of incident"""

    pass


class DutyId(EntityId):
    """ID of duty"""

    pass

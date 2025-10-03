from uuid import UUID

from sqlalchemy.orm import Mapped, declared_attr, mapped_column

from to_the_hell.oncallhub.domain.value_objects.incident_priority import (
    IncidentPriority,
)

from .base import AbstractORM


class IncidentORM(AbstractORM):
    @classmethod
    @declared_attr.directive
    def __tablename__(cls) -> str:
        return "incidents"

    description: Mapped[str] = mapped_column(nullable=False)
    incident_created: Mapped[float] = mapped_column(nullable=False)
    incident_assigned: Mapped[float | None] = mapped_column(nullable=True)
    status: Mapped[str] = mapped_column(nullable=False, default=True)
    priority: Mapped[IncidentPriority] = mapped_column(nullable=False, default=True)
    assigned_duty: Mapped[list[UUID]] = mapped_column(nullable=True)

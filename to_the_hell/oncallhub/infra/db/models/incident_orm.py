from datetime import UTC, datetime
from typing import TYPE_CHECKING

from sqlalchemy.orm import Mapped, mapped_column, relationship

from to_the_hell.oncallhub.domain.value_objects.incident_priority import (
    IncidentPriority,
)
from to_the_hell.oncallhub.infra.db.models import AbstractORM

if TYPE_CHECKING:
    from to_the_hell.oncallhub.infra.db.models import DutyORM, IncidentDutyORM


class IncidentORM(AbstractORM):
    """
    Incident ORM model with integer primary key
    """

    __tablename__ = "incidents"

    title: Mapped[str] = mapped_column(nullable=False)
    description: Mapped[str] = mapped_column(nullable=False)
    status: Mapped[str] = mapped_column(nullable=False, default="new")
    priority: Mapped[IncidentPriority] = mapped_column(nullable=False)
    created_at: Mapped[datetime] = mapped_column(default=datetime.now(UTC))
    updated_at: Mapped[datetime | None] = mapped_column(nullable=True)
    resolved_at: Mapped[datetime | None] = mapped_column(nullable=True)
    closed_at: Mapped[datetime | None] = mapped_column(nullable=True)

    incident_duties: Mapped[list["IncidentDutyORM"]] = relationship(
        back_populates="incident"
    )

    @property
    def current_duties(self) -> list["DutyORM"]:
        """Get all duties currently assigned to this incident"""
        return [id_assoc.duty for id_assoc in self.incident_duties]

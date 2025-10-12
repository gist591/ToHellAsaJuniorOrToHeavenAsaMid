from datetime import datetime
from typing import TYPE_CHECKING

from sqlalchemy.orm import Mapped, mapped_column, relationship

from to_the_hell.oncallhub.domain.value_objects.incident_priority import (
    IncidentPriority,
)

from .base import AbstractORM

if TYPE_CHECKING:
    from .duty import DutyORM
    from .incident_duty import IncidentDutyORM


class IncidentORM(AbstractORM):
    __tablename__ = "incidents"

    title: Mapped[str] = mapped_column(nullable=False)
    description: Mapped[str] = mapped_column(nullable=False)
    status: Mapped[str] = mapped_column(nullable=False, default="new")
    priority: Mapped[IncidentPriority] = mapped_column(nullable=False)
    created_at: Mapped[datetime] = mapped_column(default=datetime.utcnow)
    updated_at: Mapped[datetime | None] = mapped_column(nullable=True)
    resolved_at: Mapped[datetime | None] = mapped_column(nullable=True)
    closed_at: Mapped[datetime | None] = mapped_column(nullable=True)

    incident_duties: Mapped[list["IncidentDutyORM"]] = relationship(
        back_populates="incident"
    )

    @property
    def current_duties(self) -> list["DutyORM"]:
        return [id_assoc.duty for id_assoc in self.incident_duties]

from datetime import datetime
from typing import TYPE_CHECKING
from uuid import UUID

from sqlalchemy import DateTime, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from to_the_hell.oncallhub.infra.db.models.incident import IncidentORM

from .base import AbstractORM

if TYPE_CHECKING:
    from .devops import DevopsORM
    from .incident_duty import IncidentDutyORM


class DutyORM(AbstractORM):
    """Duty schedule model"""

    __tablename__ = "duties"

    devops_id: Mapped[UUID] = mapped_column(ForeignKey("devopses.id"))
    start_time: Mapped[datetime] = mapped_column(nullable=False)
    end_time: Mapped[datetime] = mapped_column()
    status: Mapped[bool] = mapped_column(nullable=False, default=True)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=datetime.utcnow, nullable=False
    )

    user: Mapped["DevopsORM"] = relationship(back_populates="duties")

    incident_duties: Mapped[list["IncidentDutyORM"]] = relationship(
        back_populates="duty", cascade="all, delete-orphan"
    )

    @property
    def incidents(self) -> list["IncidentORM"]:
        return [id_assoc.incident for id_assoc in self.incident_duties]

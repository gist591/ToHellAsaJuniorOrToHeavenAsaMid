from datetime import UTC, datetime
from typing import TYPE_CHECKING

from sqlalchemy import DateTime, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from to_the_hell.oncallhub.infra.db.models.base_orm import AbstractORM

if TYPE_CHECKING:
    from to_the_hell.oncallhub.infra.db.models.devops_orm import DevopsORM
    from to_the_hell.oncallhub.infra.db.models.incident_duty_orm import IncidentDutyORM
    from to_the_hell.oncallhub.infra.db.models.incident_orm import IncidentORM


class DutyORM(AbstractORM):
    """
    Duty schedule ORM model with integer IDs
    """

    __tablename__ = "duties"

    devops_id: Mapped[int] = mapped_column(ForeignKey("devopses.id"))
    start_time: Mapped[datetime] = mapped_column(nullable=False)
    end_time: Mapped[datetime] = mapped_column()
    status: Mapped[bool] = mapped_column(nullable=False, default=True)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=datetime.now(UTC), nullable=False
    )

    reminder_24h_sent: Mapped[bool] = mapped_column(default=False, nullable=False)
    reminder_2h_sent: Mapped[bool] = mapped_column(default=False, nullable=False)
    reminder_10m_sent: Mapped[bool] = mapped_column(default=False, nullable=False)

    devops: Mapped["DevopsORM"] = relationship(back_populates="duties")

    incident_duties: Mapped[list["IncidentDutyORM"]] = relationship(
        back_populates="duty", cascade="all, delete-orphan"
    )

    @property
    def incidents(self) -> list["IncidentORM"]:
        """Get all incidents associated with this duty"""
        return [id_assoc.incident for id_assoc in self.incident_duties]

    user: Mapped["DevopsORM"] = relationship(back_populates="duties")

from datetime import UTC, datetime
from typing import TYPE_CHECKING

from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from to_the_hell.oncallhub.infra.db.models.base_orm import AbstractORM

if TYPE_CHECKING:
    from to_the_hell.oncallhub.infra.db.models.duty_orm import DutyORM
    from to_the_hell.oncallhub.infra.db.models.incident_orm import IncidentORM


class IncidentDutyORM(AbstractORM):
    """
    Association table between incidents and duties
    """

    __tablename__ = "incident_duty"

    incident_id: Mapped[int] = mapped_column(ForeignKey("incidents.id"), nullable=False)
    duty_id: Mapped[int] = mapped_column(ForeignKey("duties.id"), nullable=False)
    assigned_at: Mapped[datetime] = mapped_column(
        default=datetime.now(UTC), nullable=False
    )
    assigned_by: Mapped[int | None] = mapped_column(
        ForeignKey("devopses.id"), nullable=True
    )

    notes: Mapped[str | None] = mapped_column(nullable=True)

    incident: Mapped["IncidentORM"] = relationship(back_populates="incident_duties")
    duty: Mapped["DutyORM"] = relationship(back_populates="incident_duties")

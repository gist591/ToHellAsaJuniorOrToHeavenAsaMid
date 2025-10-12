from datetime import datetime
from typing import TYPE_CHECKING
from uuid import UUID

from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base import AbstractORM

if TYPE_CHECKING:
    from .duty import DutyORM
    from .incident import IncidentORM


class IncidentDutyORM(AbstractORM):
    """Correlation table between incidents and shifts"""

    __tablename__ = "incident_duty"

    incident_id: Mapped[UUID] = mapped_column(
        ForeignKey("incidents.id"), nullable=False
    )
    duty_id: Mapped[UUID] = mapped_column(ForeignKey("duties.id"), nullable=False)
    assigned_at: Mapped[datetime] = mapped_column(
        default=datetime.utcnow, nullable=False
    )
    assigned_by: Mapped[UUID | None] = mapped_column(
        ForeignKey("devopses.id"), nullable=True
    )

    notes: Mapped[str | None] = mapped_column(nullable=True)

    incident: Mapped["IncidentORM"] = relationship(back_populates="incident_duties")
    duty: Mapped["DutyORM"] = relationship(back_populates="incident_duties")

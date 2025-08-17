from datetime import datetime

from sqlalchemy import (
    Mapped,
    mapped_column,
)

from .base import AbstractORM


class IncidentORM(AbstractORM):
    __tablename__ = "incidents"

    description: Mapped[str] = mapped_column(nullable=False)
    time_start_event: Mapped[datetime] = mapped_column(nullable=False)
    status: Mapped[bool] = mapped_column(nullable=False)

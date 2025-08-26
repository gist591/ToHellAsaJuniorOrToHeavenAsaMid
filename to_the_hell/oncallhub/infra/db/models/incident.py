from datetime import datetime

from sqlalchemy.orm import Mapped, declared_attr, mapped_column

from .base import AbstractORM


class IncidentORM(AbstractORM):
    @classmethod
    @declared_attr  # type: ignore[misc]
    def __tablename__(cls) -> str:
        return "incidents"

    description: Mapped[str] = mapped_column(nullable=False)
    time_start_event: Mapped[datetime] = mapped_column(nullable=False)
    time_end_event: Mapped[datetime | None] = mapped_column(nullable=True)
    status: Mapped[bool] = mapped_column(nullable=False, default=True)

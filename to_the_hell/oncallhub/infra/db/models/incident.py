from sqlalchemy.orm import Mapped, declared_attr, mapped_column

from .base import AbstractORM


class IncidentORM(AbstractORM):
    @classmethod
    @declared_attr  # type: ignore[misc]
    def __tablename__(cls) -> str:
        return "incidents"

    id: Mapped[id] = mapped_column(autoincrement=True, nullable=False)
    description: Mapped[str] = mapped_column(nullable=False)
    incident_created: Mapped[float] = mapped_column(nullable=False)
    incident_assigned: Mapped[float | None] = mapped_column(nullable=True)
    status: Mapped[str] = mapped_column(nullable=False, default=True)
    priority: Mapped[int] = mapped_column(nullable=False, default=True)
    assigned_duty: Mapped[list] = mapped_column(nullable=True)

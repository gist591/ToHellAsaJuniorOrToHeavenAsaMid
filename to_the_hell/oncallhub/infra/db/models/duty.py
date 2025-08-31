from datetime import datetime

from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, declared_attr, mapped_column, relationship

from .base import AbstractORM


class DutyORM(AbstractORM):
    @classmethod
    @declared_attr  # type: ignore[misc]
    def __tablename__(cls) -> str:
        return "duties"

    user_id: Mapped[int] = mapped_column(ForeignKey("devopses.id"))
    start_time: Mapped[datetime] = mapped_column(nullable=False)
    end_time: Mapped[datetime] = mapped_column()
    status: Mapped[bool] = mapped_column(nullable=False)

    user: Mapped[UserORM] = relationship(back_populates="duties")

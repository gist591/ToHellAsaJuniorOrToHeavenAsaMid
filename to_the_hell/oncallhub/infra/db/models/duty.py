from datetime import datetime
from typing import TYPE_CHECKING
from uuid import UUID

from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, declared_attr, mapped_column, relationship

from .base import AbstractORM

if TYPE_CHECKING:
    from .devops import DevopsORM


class DutyORM(AbstractORM):
    @classmethod
    @declared_attr.directive
    def __tablename__(cls) -> str:
        return "duties"

    user_id: Mapped[UUID] = mapped_column(ForeignKey("devopses.id"))
    start_time: Mapped[datetime] = mapped_column(nullable=False)
    end_time: Mapped[datetime] = mapped_column()
    status: Mapped[bool] = mapped_column(nullable=False)

    user: Mapped[DevopsORM] = relationship(back_populates="duties")

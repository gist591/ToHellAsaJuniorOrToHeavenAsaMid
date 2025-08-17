from datetime import datetime

from sqlalchemy import (
    ForeignKey,
    Mapped,
    mapped_column,
)
from sqlalchemy.orm import relationship

from .base import AbstractORM


class DutyORM(AbstractORM):
    __tablename__ = "duties"

    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    start_time: Mapped[datetime] = mapped_column(nullable=False)
    end_time: Mapped[datetime] = mapped_column()
    status: Mapped[bool] = mapped_column(nullable=False)

    user = relationship("UserORM")

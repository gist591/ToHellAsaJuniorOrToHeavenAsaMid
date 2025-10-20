from typing import TYPE_CHECKING

from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base import AbstractORM

if TYPE_CHECKING:
    from .duty import DutyORM


class DevopsORM(AbstractORM):
    """DevOps user model"""

    __tablename__ = "devopses"

    name: Mapped[str] = mapped_column(nullable=False)
    telegram_username: Mapped[str] = mapped_column(unique=True, nullable=False)
    email: Mapped[str] = mapped_column(nullable=False)
    phone: Mapped[str] = mapped_column(nullable=False)

    duties: Mapped[list["DutyORM"]] = relationship(back_populates="devops")

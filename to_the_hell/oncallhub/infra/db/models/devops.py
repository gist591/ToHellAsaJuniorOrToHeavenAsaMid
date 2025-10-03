from sqlalchemy.orm import Mapped, declared_attr, mapped_column, relationship

from .base import AbstractORM
from .duty import DutyORM


class DevopsORM(AbstractORM):
    @classmethod
    @declared_attr.directive
    def __tablename__(cls) -> str:
        return "devopses"

    name: Mapped[str] = mapped_column()
    telegram_username: Mapped[str] = mapped_column(unique=True, nullable=False)

    duties: Mapped[list[DutyORM]] = relationship(back_populates="devops")

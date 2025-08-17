from sqlalchemy import Mapped, mapped_column

from .base import AbstractORM


class UserORM(AbstractORM):
    __tablename__ = "users"

    name: Mapped[str] = mapped_column()
    telegram_username: Mapped[str] = mapped_column(unique=True, nullable=False)

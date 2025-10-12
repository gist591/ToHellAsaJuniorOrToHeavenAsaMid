from uuid import UUID

from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column


class Base(DeclarativeBase):
    pass


class AbstractORM(Base):
    """Base class for ORM models"""

    __abstract__ = True

    id: Mapped[UUID] = mapped_column(autoincrement=True, primary_key=True)

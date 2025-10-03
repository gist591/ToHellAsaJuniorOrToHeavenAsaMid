from uuid import UUID

from sqlalchemy.orm import DeclarativeBase, Mapped, declared_attr, mapped_column


class Base(DeclarativeBase):
    pass


class AbstractORM(Base):
    """Base class for ORM models"""

    id: Mapped[UUID] = mapped_column(autoincrement=True, primary_key=True)

    @classmethod
    @declared_attr.directive
    def __tablename__(cls) -> str:
        return cls.__name__.lower()

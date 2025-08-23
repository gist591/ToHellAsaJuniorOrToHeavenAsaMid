from sqlalchemy.orm import DeclarativeBase, Mapped, declared_attr, mapped_column


class Base(DeclarativeBase):  # type: ignore[misc]
    pass


class AbstractORM(Base):
    """Base class for ORM models"""

    id: Mapped[int] = mapped_column(autoincrement=True, primary_key=True)

    @classmethod
    @declared_attr  # type: ignore[misc]
    def __tablename__(cls) -> str:
        return cls.__name__.lower()

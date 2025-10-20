from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column


class Base(DeclarativeBase):
    """
    Base class for all database models
    """

    pass


class AbstractORM(Base):
    """
    Base class for ORM models with integer primary key
    """

    __abstract__ = True

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)

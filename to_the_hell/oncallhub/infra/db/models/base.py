from sqlalchemy.orm import as_declarative, mapped_column, Mapped, declared_attr
from sqlalchemy import Integer, String


@as_declarative()
class AbstractORM():
    id: Mapped[int] = mapped_column(autoincrement=True, primary_key=True)

    @classmethod
    @declared_attr
    def __tablename__(cls):
        return cls.__name__.lower()

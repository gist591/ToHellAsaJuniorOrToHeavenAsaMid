from sqlalchemy.orm import Mapped, as_declarative, declared_attr, mapped_column


@as_declarative()
class AbstractORM:
    id: Mapped[int] = mapped_column(autoincrement=True, primary_key=True)

    @classmethod
    @declared_attr
    def __tablename__(cls):
        return cls.__name__.lower()

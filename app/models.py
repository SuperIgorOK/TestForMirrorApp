from datetime import datetime

from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, relationship, mapped_column, DeclarativeBase, declared_attr


class Base(DeclarativeBase):
    __abstract__ = True

    @declared_attr.directive
    def __tablename__(cls) -> str:
        return f"{cls.__name__.lower()}s"

    id: Mapped[int] = mapped_column(primary_key=True)



class Walker(Base):
    name: Mapped[str]
    # relations
    walks: Mapped[list["Walk"]] = relationship("Walk", back_populates="walker")


class Walk(Base):
    apartment_number: Mapped[int]
    pet_name: Mapped[str]
    pet_breed: Mapped[str]
    start_time: Mapped[datetime]
    end_time: Mapped[datetime]
    walker_id: Mapped[int] = mapped_column(ForeignKey("walkers.id"))
    # relations
    walker: Mapped["Walker"] = relationship("Walker", back_populates="walks")

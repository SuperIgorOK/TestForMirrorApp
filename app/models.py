from datetime import datetime

from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, relationship, mapped_column

from app.db import Base


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

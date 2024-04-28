from datetime import timedelta, datetime

from sqlalchemy import select, Result, func
from sqlalchemy.orm import Session

from app.models import Walk, Walker
from app.schemas import WalkCreate


def get_walks(session: Session) -> list[Walk] | None:
    stmt = select(Walk).order_by(Walk.start_time)
    result: Result = session.execute(stmt)
    walks = result.scalars().all()
    return list(walks)


def get_walks_by_date(date: datetime, session: Session) -> list[Walk] | None:
    stmt = select(Walk).where(func.date(Walk.start_time) == date.date())
    result: Result = session.execute(stmt)
    walks = result.scalars().all()
    return list(walks)


def create_walk(session: Session, walk: WalkCreate, walker_id: int):
    walk = Walk(
        apartment_number=walk.apartment_number,
        pet_name=walk.pet_name,
        pet_breed=walk.pet_breed,
        start_time=walk.start_time,
        end_time=walk.start_time + timedelta(minutes=30),
        walker_id=walker_id
    )
    session.add(walk)
    session.commit()
    session.refresh(walk)
    return walk


def create_walkers(session: Session):
    walker1 = Walker(name="Петр")
    walker2 = Walker(name="Антон")
    session.add_all([walker1, walker2])
    session.commit()

from datetime import datetime
from fastapi import HTTPException
from datetime import time

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.crud import create_walkers
from app.models import Walk, Walker


def check_workers(session: Session):
    walkers = session.execute(select(Walker)).first()

    if not walkers:
        create_walkers(session)


def validate_walk_start_minute(walk_start_time: datetime):
    if walk_start_time.minute not in (0, 30):
        raise HTTPException(
            status_code=400,
            detail="Walk can start either on the hour or half-hour only."
        )


def validate_walk_time_range(walk_start_time: datetime):
    if not (time(7, 00) <= walk_start_time.time() <= time(23, 00)):
        raise HTTPException(
            status_code=400,
            detail="Walk can be scheduled between 7 AM and 11 PM only."
        )


def get_available_walker_id(
        session: Session,
        walk_start_time: datetime
) -> int:
    # Проверка на существующие прогулки в это время
    current_walks = session.query(Walk).filter(
        Walk.start_time == walk_start_time
    ).count()
    if current_walks >= 2:
        raise HTTPException(status_code=400, detail="No available walkers.")
    return 1 if current_walks == 0 else 2

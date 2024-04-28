from datetime import datetime
from fastapi import HTTPException
from datetime import time

from sqlalchemy import select, Result, func
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
            detail="Прогулка может начинаться либо в начале часа, либо в полчаса."
        )


def validate_walk_time_range(walk_start_time: datetime):
    if not (time(7, 00) <= walk_start_time.time() <= time(23, 00)):
        raise HTTPException(
            status_code=400,
            detail="Прогулка может быть с 7:00 до 23:00."
        )


def get_available_walker_id(
        session: Session,
        walk_start_time: datetime
) -> int:
    # Проверка на существующие прогулки в это время
    stmt = select(func.count()).where(Walk.start_time == walk_start_time)
    current_walks = session.execute(stmt).scalar()
    if current_walks >= 2:
        raise HTTPException(status_code=400, detail="Нет свободного выгульщика.")
    return 1 if current_walks == 0 else 2

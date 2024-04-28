from datetime import datetime
from typing import Annotated

import uvicorn
from fastapi import FastAPI, Depends, Path
from sqlalchemy.orm import Session
from fastapi.responses import RedirectResponse

from app import models, schemas, crud
from app.db import engine, get_db
from app.validators import (
    validate_walk_start_minute,
    validate_walk_time_range,
    get_available_walker_id, check_workers
)
from app.models import Walk


models.Base.metadata.create_all(bind=engine)

app = FastAPI()


@app.get("/")
def redirect_todo():
    return RedirectResponse(url="/docs/", status_code=302)


@app.on_event("startup")
async def startup_event():
    check_workers(session=next(get_db()))


@app.get("/walks/{date}/", response_model=list[schemas.Walk])
def get_walks_by_date(
        date: Annotated[datetime, Path],
        session: Session = Depends(get_db)
) -> list[Walk] | None:
    return crud.get_walks_by_date(date, session)


# Получить все созданные прогулки
@app.get("/walks/", response_model=list[schemas.Walk])
def get_all_walks(
        session: Session = Depends(get_db),
):
    return crud.get_walks(session=session)


@app.post("/walks/", response_model=schemas.Walk)
def create_walk(
        walk: schemas.WalkCreate,
        session: Session = Depends(get_db)
) -> Walk:
    # Валидация времени прогулки
    validate_walk_start_minute(walk.start_time)
    validate_walk_time_range(walk.start_time)

    # Проверка наличия свободных выгульщиков
    walker_id = get_available_walker_id(session, walk.start_time)

    return crud.create_walk(session, walk, walker_id)


if __name__ == "__main__":
    uvicorn.run("main:app", port=8080, reload=True)

from pydantic import BaseModel, ConfigDict
from datetime import datetime


class WalkBase(BaseModel):
    apartment_number: int
    pet_name: str
    pet_breed: str


class WalkCreate(WalkBase):
    start_time: datetime


class Walk(WalkBase):
    model_config = ConfigDict(from_attributes=True)
    id: int
    start_time: datetime
    walker_id: int


class WalkerBase(BaseModel):
    id: int
    name: str


class Walker(WalkerBase):
    model_config = ConfigDict(from_attributes=True)
    walks: list[Walk] = []

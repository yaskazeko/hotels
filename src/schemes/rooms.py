from typing import Optional

from src.models import RoomOrm
from src.schemes.facilities import Facility

from pydantic import BaseModel, Field, confloat, conint


class RoomBase(BaseModel):
    name: str = Field(..., max_length=120)
    description: Optional[str] = None
    capacity: conint(ge=1) = 2
    price_per_night: confloat(ge=0) = 0.0
    is_active: bool = True
    facilities_ids: list[int] | None = None

class RoomCreate(RoomBase):
    hotel_id: int




class RoomUpdate(BaseModel):
    name: Optional[str] = Field(None, max_length=120)
    description: Optional[str] = None
    capacity: Optional[conint(ge=1)] = None
    price_per_night: Optional[confloat(ge=0)] = None
    is_active: Optional[bool] = None
    facilities_ids: list[int] | None = None

class RoomInDB(RoomBase):
    id: int
    hotel_id: int

    class Config:
        from_attributes = True

class RoomWithRels(BaseModel):
    id: int
    hotel_id: int
    name: str
    description: Optional[str] = None
    capacity: int
    price_per_night: float
    is_active: bool
    facilities: list[Facility]

    class Config:
        from_attributes = True

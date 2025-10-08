from datetime import date
from pydantic.config import ConfigDict
from pydantic import BaseModel



class BookingsBase(BaseModel):
    room_id: int
    date_from: date
    date_to: date
    price: float

class BookingsCreate(BookingsBase):
    room_id: int
    price: float

class BookingOut(BookingsBase):
    id: int
    price: float
    model_config = ConfigDict(from_attributes=True)
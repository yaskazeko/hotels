from datetime import date

from pydantic import BaseModel, ConfigDict, Field, field_validator


class BookingsBase(BaseModel):
    room_id: int = Field(gt=0, description="Room ID must be positive")
    date_from: date = Field(description="Check-in date")
    date_to: date = Field(description="Check-out date")
    price: float = Field(gt=0, description="Price per night")

    @field_validator('date_to')
    @classmethod
    def validate_dates(cls, date_to: date, info) -> date:
        date_from = info.data.get('date_from')
        if date_from and date_to <= date_from:
            raise ValueError('Check-out date must be after check-in date')
        return date_to

    @field_validator('date_from')
    @classmethod
    def validate_date_from(cls, date_from: date) -> date:
        if date_from < date.today():
            raise ValueError('Check-in date cannot be in the past')
        return date_from


class BookingsCreate(BaseModel):
    room_id: int = Field(gt=0, description="Room ID must be positive")
    date_from: date = Field(description="Check-in date")
    date_to: date = Field(description="Check-out date")
    price: float = Field(gt=0, description="Price per night")

    @field_validator('date_to')
    @classmethod
    def validate_dates(cls, date_to: date, info) -> date:
        date_from = info.data.get('date_from')
        if date_from and date_to <= date_from:
            raise ValueError('Check-out date must be after check-in date')
        return date_to

    @field_validator('date_from')
    @classmethod
    def validate_date_from(cls, date_from: date) -> date:
        if date_from < date.today():
            raise ValueError('Check-in date cannot be in the past')
        return date_from


class BookingOut(BookingsBase):
    id: int
    user_id: int
    total_days: int | None = None
    total_price: float | None = None

    model_config = ConfigDict(from_attributes=True)
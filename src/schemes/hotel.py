from pydantic import BaseModel, Field

class Hotel(BaseModel):
    title: str
    phone: str

class HotelPatch(BaseModel):
    title: str | None = Field(None)
    phone: str | None = Field(None)
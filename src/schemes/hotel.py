from pydantic import BaseModel, Field, ConfigDict

class Hotel(BaseModel):
    title: str
    phone: str
    location: str

    model_config = ConfigDict(from_attributes=True)

class HotelPatch(BaseModel):
    title: str | None = Field(None)
    phone: str | None = Field(None)
    location: str | None = Field(None)
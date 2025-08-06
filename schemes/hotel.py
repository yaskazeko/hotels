from pydantic import BaseModel, Field




class Hotel(BaseModel):
    title: str
    phone: str

class Hotel_patch(BaseModel):
    title: str | None = Field(None)
    phone: str | None = (None)
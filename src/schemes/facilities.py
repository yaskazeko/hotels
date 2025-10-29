from pydantic import BaseModel, Field


class FacilitiesBase(BaseModel):
    title: str = Field(..., max_length=100)


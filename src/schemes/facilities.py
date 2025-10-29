from pydantic import BaseModel, Field


class FacilitiesBase(BaseModel):
    title: str = Field(..., max_length=100)

class RoomFacilitiesAdd(BaseModel):
    room_id: int
    facility_id: int

class RoomFacilities(RoomFacilitiesAdd):
    id: int

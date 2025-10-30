from pydantic import BaseModel, Field, ConfigDict


class FacilitiesAdd(BaseModel):
    title: str = Field(..., max_length=100)

class Facility(FacilitiesAdd):
    id: int

    model_config = ConfigDict(from_attributes=True)

class RoomFacilitiesAdd(BaseModel):
    room_id: int
    facility_id: int

class RoomFacilities(RoomFacilitiesAdd):
    id: int

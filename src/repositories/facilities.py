from sqlalchemy import delete, select
from sqlalchemy.ext.asyncio import AsyncSession
from src.models.facilities import FacilitiesOrm, RoomsFacilitiesOrm
from src.repositories.base import BaseRepository
from src.schemes.facilities import FacilitiesAdd, RoomFacilities, RoomFacilitiesAdd


class FacilitiesRepository(BaseRepository):

    async def get(
            self,
            facility_id: int,
    ):
        query = select(FacilitiesOrm).where(FacilitiesOrm.id == facility_id)
        result = await self.session.execute(query)
        return result.scalar_one_or_none()


    async def create(self, data: FacilitiesAdd) -> FacilitiesOrm:
        facility = FacilitiesOrm(**data.model_dump())
        self.session.add(facility)
        await self.session.flush()  # чтобы получить facility.id
        return facility

class RoomFacilitiesRepository(BaseRepository):
    model = RoomsFacilitiesOrm
    schema = RoomFacilities




    async def set_room_facilities(self, room_id: int, facilities_ids: list[int]):
        await self.session.execute(
            delete(RoomsFacilitiesOrm).where(RoomsFacilitiesOrm.room_id == room_id)
        )
        if facilities_ids:
            rooms_facilities_data = [
                RoomFacilitiesAdd(room_id=room_id, facility_id=f_id)
                for f_id in facilities_ids
            ]
            await self.add_bulk(rooms_facilities_data)
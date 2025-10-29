from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from src.models.facilities import FacilitiesOrm
from src.schemes.facilities import FacilitiesBase

class FacilitiesRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def get(
            self,
            facility_id: int,
    ):
        query = select(FacilitiesOrm).where(FacilitiesOrm.id == facility_id)
        result = await self.session.execute(query)
        return result.scalar_one_or_none()


    async def create(self, data: FacilitiesBase) -> FacilitiesOrm:
        facility = FacilitiesOrm(**data.model_dump())
        self.session.add(facility)
        await self.session.flush()  # чтобы получить facility.id
        return facility
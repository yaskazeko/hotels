from sqlalchemy import select, insert, update, delete

from src.models.hotels import HotelsOrm
from src.repositories.base import BaseRepository
from src.schemes.hotel import Hotel


class HotelsRepository(BaseRepository):
    model = HotelsOrm

    async def get_all_hotels(
            self,
            title: str = None,
            offset: int = None,
            limit: int = None,
            **kwargs
    ):
        query = select(HotelsOrm)
        if title:
            query = query.filter(HotelsOrm.title.ilike(f" %{title}%"))
        query = (
            query
            .limit(limit)
            .offset(offset)
        )
        result = await self.session.execute(query)
        return result.scalars().all()


    async def post_hotels(
            self,
            hotel_data: Hotel = None,
    ) -> HotelsOrm:
        obj = HotelsOrm(**hotel_data.model_dump())
        self.session.add(obj)
        return obj
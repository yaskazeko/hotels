from http.client import HTTPException

from pydantic import BaseModel
from requests import Session
from sqlalchemy import delete, insert, select, update

from src.api import Hotels
#from src.api.Hotels import hotels
from src.models.hotels import HotelsOrm
from src.repositories.base import BaseRepository
from src.schemes.hotel import Hotel


class HotelsRepository(BaseRepository):
    model = HotelsOrm
    schema:BaseModel = Hotel


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

        return [self.schema.model_validate(model) for model in result.scalars().all()]

    async def get(
            self,
            hotel_id: int,
    ):
        query = select(HotelsOrm, hotel_id)
        result = await self.session.execute(query)
        return result.scalar()

    async def post_hotels(
            self,
            hotel_data: Hotel = None,
    ) -> HotelsOrm:
        obj = HotelsOrm(**hotel_data.model_dump())
        self.session.add(obj)
        return obj

    async def put_hotel(
            self,
            hotel_id: int,
            hotel_data: Hotel = None,
    ) -> HotelsOrm | None:
        obj = await self.session.get(HotelsOrm, hotel_id)
        if obj is None:
            return None
        for key, value in hotel_data.model_dump().items():
            if key == "id":
                continue
            setattr(obj, key, value)
        return obj


    async def patch_hotel(self, obj: HotelsOrm, data: dict) -> HotelsOrm:
        allowed = {c.name for c in HotelsOrm.__table__.columns}
        for k, v in data.items():
            if k in allowed:
                setattr(obj, k, v)
        self.session.add(obj)
        return obj


    async def delete_hotels(
            self,
            hotel_id: int,
    ) -> bool:
        obj = await self.session.get(HotelsOrm, hotel_id)
        if obj is None:
            return False
        await self.session.delete(obj)
        return True
    async def flush(self): await self.session.flush()
    async def refresh(self, obj): await self.session.refresh(obj)
    async def commit(self): await self.session.commit()
    async def rollback(self): await self.session.rollback()
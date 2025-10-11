from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from sqlalchemy.orm import selectinload

from src.schemes.rooms import RoomCreate
from src.models.booking import BookingsOrm
from src.schemes.bookings import BookingsCreate
class BookingsRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def createbookings(self, data: BookingsCreate) -> BookingsOrm:
        bookings = BookingsOrm(**data.model_dump())
        self.session.add(bookings)
        await self.session.flush()
        return bookings

    async def get_all(self, skip: int = 0, limit: int = 10) -> list[BookingsOrm]:
        query = select(BookingsOrm).offset(skip).limit(limit)
        result = await self.session.execute(query)
        return list(result.scalars().all())

    async def get_user_bookings(self, user_id: int) -> list[BookingsOrm]:
        query = select(BookingsOrm).where(BookingsOrm.user_id == user_id)
        result = await self.session.execute(query)
        return list(result.scalars().all())
    
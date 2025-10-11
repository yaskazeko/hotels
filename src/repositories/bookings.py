from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from src.models.booking import BookingsOrm
from src.schemes.bookings import BookingsCreate


class BookingsRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def create_booking(self, data: BookingsCreate, user_id: int) -> BookingsOrm:
        booking_data = data.model_dump()
        booking_data['user_id'] = user_id
        booking = BookingsOrm(**booking_data)
        self.session.add(booking)
        await self.session.flush()
        return booking

    async def get_all(self, skip: int = 0, limit: int = 10) -> list[BookingsOrm]:
        query = (
            select(BookingsOrm)
            .options(selectinload(BookingsOrm.user), selectinload(BookingsOrm.room))
            .offset(skip)
            .limit(limit)
        )
        result = await self.session.execute(query)
        return list(result.scalars().all())

    async def get_user_bookings(self, user_id: int) -> list[BookingsOrm]:
        query = (
            select(BookingsOrm)
            .where(BookingsOrm.user_id == user_id)
            .options(selectinload(BookingsOrm.room))
        )
        result = await self.session.execute(query)
        return list(result.scalars().all())
    
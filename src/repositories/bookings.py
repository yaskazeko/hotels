from sqlalchemy.ext.asyncio import AsyncSession

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
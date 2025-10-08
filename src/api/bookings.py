from datetime import date

from fastapi import APIRouter, Depends, HTTPException, status
from src.api.Dependencies import DBDep
from src.models.booking import BookingsOrm
from src.schemes.bookings import BookingsCreate, BookingOut

router = APIRouter(prefix="/bookings", tags=["Bookings"])


@router.post("", response_model=BookingOut, status_code=status.HTTP_201_CREATED)
async def create_bookings(
        db: DBDep,
        data: BookingsCreate,
):
    bookings = await db.bookings.createbookings(data)
    if not bookings:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Booking not found")
    await db.commit()
    return bookings
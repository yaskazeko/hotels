from typing import List

from fastapi import APIRouter, HTTPException, status

from src.api.dependencies import CurrentUserDep, DBDep
from src.schemes.bookings import BookingOut, BookingsCreate

router = APIRouter(prefix="/bookings", tags=["Bookings"])


@router.get("", response_model=List[BookingOut])
async def get_all_bookings(
    db: DBDep,
    skip: int = 0,
    limit: int = 10,
):
    bookings = await db.bookings.get_all(skip=skip, limit=limit)
    return bookings


@router.get("/me", response_model=List[BookingOut])
async def get_user_bookings(
    db: DBDep,
    current_user_id: CurrentUserDep,
):
    bookings = await db.bookings.get_user_bookings(current_user_id)
    if not bookings:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No bookings found for this user")
    return bookings


@router.post("", response_model=BookingOut, status_code=status.HTTP_201_CREATED)
async def create_booking(
    db: DBDep,
    current_user_id: CurrentUserDep,
    data: BookingsCreate,
):
    booking = await db.bookings.createbookings(data)
    if not booking:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Failed to create booking")
    await db.commit()
    return booking
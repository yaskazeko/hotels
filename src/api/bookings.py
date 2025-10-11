from fastapi import APIRouter, HTTPException, status
from typing import List
from src.api.dependencies import DBDep
from pydantic import EmailStr
from src.schemes.bookings import BookingsCreate, BookingOut

router = APIRouter(prefix="/bookings", tags=["Bookings"])


@router.get("/bookings", response_model=List[BookingOut])
async def get_all_bookings(
        db: DBDep,
        skip: int = 0,
        limit: int = 10,
):
    bookings = await db.bookings.get_all(skip=skip, limit=limit)
    return bookings


@router.get("/bookings/me", response_model=List[BookingOut])
async def get_user_bookings(
        db: DBDep,
        current_user: EmailStr,
):
    bookings = await db.bookings.get_by_user_id(current_user)
    if not bookings:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No bookings found for this user")
    return bookings


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
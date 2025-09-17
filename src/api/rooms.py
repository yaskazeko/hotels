from typing import List, Optional

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.ext.asyncio import AsyncSession

from src.database import get_async_session  # твой провайдер сессии
from src.repositories.rooms import RoomsRepository
from src.schemes.rooms import RoomCreate, RoomInDB, RoomUpdate

router = APIRouter(prefix="/rooms", tags=["rooms"])

# GET /rooms — список с фильтрами и пагинацией
@router.get("", response_model=List[RoomInDB])
async def list_rooms(
    hotel_id: Optional[int] = Query(None),
    min_price: Optional[float] = Query(None, ge=0),
    max_price: Optional[float] = Query(None, ge=0),
    capacity: Optional[int] = Query(None, ge=1),
    is_active: Optional[bool] = Query(True),
    limit: int = Query(50, ge=1, le=200),
    offset: int = Query(0, ge=0),
    order_by_price: Optional[str] = Query(None, pattern="^(asc|desc)$"),
    session: AsyncSession = Depends(get_async_session),
):
    repo = RoomsRepository(session)
    return await repo.list(
        hotel_id=hotel_id,
        min_price=min_price,
        max_price=max_price,
        capacity=capacity,
        is_active=is_active,
        limit=limit,
        offset=offset,
        order_by_price=order_by_price,
    )

# GET /rooms/{id} — детально
@router.get("/{room_id}", response_model=RoomInDB)
async def get_room(
    room_id: int,
    session: AsyncSession = Depends(get_async_session),
):
    repo = RoomsRepository(session)
    room = await repo.get_by_id(room_id)
    if not room:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Room not found")
    return room

# POST /rooms — создать
@router.post("", response_model=RoomInDB, status_code=status.HTTP_201_CREATED)
async def create_room(
    data: RoomCreate,
    session: AsyncSession = Depends(get_async_session),
):
    repo = RoomsRepository(session)
    room = await repo.create(data)
    await session.commit()
    return room

# PATCH /rooms/{id} — частичное обновление
@router.patch("/{room_id}", response_model=RoomInDB)
async def patch_room(
    room_id: int,
    data: RoomUpdate,
    session: AsyncSession = Depends(get_async_session),
):
    repo = RoomsRepository(session)
    room = await repo.update(room_id, data)
    if not room:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Room not found")
    await session.commit()
    return room

# DELETE /rooms/{id}
@router.delete("/{room_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_room(
    room_id: int,
    session: AsyncSession = Depends(get_async_session),
):
    repo = RoomsRepository(session)
    ok = await repo.delete(room_id)
    await session.commit()
    if not ok:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Room not found")
    return None


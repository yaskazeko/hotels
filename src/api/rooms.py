from typing import List, Optional

from fastapi import APIRouter, HTTPException, Query, status

from src.api.dependencies import DBDep
from src.schemes.rooms import RoomCreate, RoomInDB, RoomUpdate

router = APIRouter(prefix="/rooms", tags=["rooms"])

# GET /rooms — список с фильтрами и пагинацией
@router.get("", response_model=List[RoomInDB])
async def list_rooms(
    db: DBDep,
    hotel_id: Optional[int] = Query(None),
    min_price: Optional[float] = Query(None, ge=0),
    max_price: Optional[float] = Query(None, ge=0),
    capacity: Optional[int] = Query(None, ge=1),
    is_active: Optional[bool] = Query(True),
    skip: int = Query(0, ge=0, description="Number of records to skip"),
    limit: int = Query(50, ge=1, le=200, description="Number of records to return"),
    order_by_price: Optional[str] = Query(None, pattern="^(asc|desc)$"),
):

    return await db.rooms.list(
        hotel_id=hotel_id,
        min_price=min_price,
        max_price=max_price,
        capacity=capacity,
        is_active=is_active,
        limit=limit,
        offset=skip,
        order_by_price=order_by_price,
    )

# GET /rooms/{id} — детально
@router.get("/{room_id}", response_model=RoomInDB)
async def get_room(
    db: DBDep,
    room_id: int,
):

    room = await db.rooms.get_by_id(room_id)
    if not room:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Room not found")
    return room

# POST /rooms — создать
@router.post("", response_model=RoomInDB, status_code=status.HTTP_201_CREATED)
async def create_room(
    db: DBDep,
    data: RoomCreate,
):
    room = await db.rooms.create(data)
    if not room:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Room not found")
    await db.commit()
    return room

# PATCH /rooms/{id} — частичное обновление
@router.patch("/{room_id}", response_model=RoomInDB)
async def patch_room(
    db: DBDep,
    room_id: int,
    data: RoomUpdate,
):
    return await db.rooms.update(room_id, data)

# DELETE /rooms/{id}
@router.delete("/{room_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_room(
    db: DBDep,
    room_id: int,
):
    ok = await db.rooms.delete(room_id)
    await db.commit()
    if not ok:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Room not found")
    return None


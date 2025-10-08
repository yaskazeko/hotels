from typing import List

from fastapi import APIRouter, Body, HTTPException, Path, Query
from sqlalchemy import insert
from sqlalchemy.exc import IntegrityError
from starlette import status

from src.api.Dependencies import PaginationDep, DBDep
from src.database import async_session_maker, engine
from src.models.hotels import HotelsOrm
from src.repositories.hotels import HotelsRepository
from src.schemes.hotel import Hotel, HotelPatch

router = APIRouter(prefix="/hotels", tags=["Hotels"])

@router.get("")
async def get_hotels(
    db: DBDep,
    pagination: PaginationDep,
    # id_hotel: int | None = Query(None, description="The ID of the hotel."),
    title: str | None = Query(None, description="The title of the hotel."),

) -> List[Hotel]:

    return await db.hotels.get_all_hotels(
        title=title,
        limit=pagination.per_page,
        offset=(pagination.page - 1)*pagination.per_page,
    )

@router.get("/{hotel_id}")
async def get_hotel(
        db: DBDep,
        hotel_id: int,
):

        return await db.hotels.get(hotel_id)


@router.post("")
async def post_hotels(
        db: DBDep,
        hotel_data: Hotel = Body(description="The hotel data.", openapi_examples={
            "1":{
                "summary": "Hotel 1",
                "value": {
                    "title": "Hilltop Inn",
                    "phone": "Не указано",
                    "location": "Berlin",
                },
            },
            "2":{
                "summary": "Hotel 2",
                "value": {
                    "title": "Atlantic Hotel",
                    "location": "Berlin",
                    "phone": "+1 410-641-3589",
                },
            },
            "3":{
                "summary": "Hotel 3",
                "value": {
                    "title": "Comfort Inn & Suites Montpelier-Berlin",
                    "location": "Berlin",
                    "phone": "+1 802-613-1120",
                },
            },
            "4":{
                "summary": "Hotel 4",
                "value": {
                    "title": "Days Inn",
                    "location": "Berlin",
                    "phone": "+1 860-438-6178",
                },
            },
            "5":{
                "summary": "Hotel 5",
                "value": {
                    "title": "Best Western Plus",
                    "location": "Berlin",
                    "phone": "+1 860-828-3000",
                },
            },
            "6":{
                "summary": "Hotel 6",
                "value": {
                    "title": "Homewood Suites by Hilton Boston Marlborough;Homewood Suites",
                    "location": "Berlin",
                    "phone": "+1 978-838-9940",
                },
            },
        })
):


    try:
        obj = await db.hotels.post_hotels(hotel_data)
        await db.flush()
        await db.refresh()
        await db.commit()
    except IntegrityError:
        await db.rollback()
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Hotel already exists or violates a constraint.",
        )
    return {
        "status": "OK",
        "data": obj,
    }



@router.put("/{id_hotel}")
async def put_hotels(
        db: DBDep,
        id_hotel: int = Path(description="The ID of the hotel."),
        hotel_data: Hotel = Body(embed=True, description="The hotel data."),
):
        repo = db.hotels
        put_hotel_ok = await repo.put_hotel(id_hotel, hotel_data)
        if not put_hotel_ok:
            raise HTTPException(status_code=404, detail="Hotel not found")
        await repo.flush()
        await repo.refresh(put_hotel_ok)
        await repo.commit()
        return {"status": "OK", "data": put_hotel_ok}

@router.patch("/{id_hotel}")
async def patch_hotels(
    db: DBDep,
    id_hotel: int = Path(description="The ID of the hotel."),
    hotel_data: HotelPatch = Body(embed=True, description="The hotel data."),
):
    repo = db.hotels
    data = hotel_data.model_dump(exclude_unset=True)

    if not data:
        raise HTTPException(status_code=400, detail="No fields to update.")

    # Загружаем объект
    obj = await repo.get(id_hotel)
    if not obj:
        raise HTTPException(status_code=404, detail="Hotel not found")

    try:
        # Частичное обновление
        await repo.patch_hotel(obj, data)

        await repo.flush()
        await repo.refresh(obj)
        await repo.commit()
    except IntegrityError:
        await repo.rollback()
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Update violates a constraint.",
        )

    return {"status": "OK", "data": obj}
@router.delete("/{hotel_id}")
async def delete_hotel(hotel_id: int):
    async with async_session_maker() as session:
        repo = HotelsRepository(session)
        ok = await repo.delete_hotels(hotel_id)
        if not ok:
            raise HTTPException(status_code=404, detail="The hotel does not exist.")

        await session.commit()
    return {"Status": "OK"}



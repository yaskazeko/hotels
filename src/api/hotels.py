from typing import List

from fastapi import APIRouter, Body, HTTPException, Path, Query, status
from sqlalchemy.exc import IntegrityError

from src.api.dependencies import DBDep
from src.schemes.hotel import Hotel, HotelPatch

router = APIRouter(prefix="/hotels", tags=["Hotels"])

@router.get("")
async def get_hotels(
    db: DBDep,
    title: str | None = Query(None, description="The title of the hotel."),
    skip: int = Query(0, ge=0, description="Number of records to skip"),
    limit: int = Query(10, ge=1, le=100, description="Number of records to return"),
) -> List[Hotel]:

    return await db.hotels.get_all_hotels(
        title=title,
        limit=limit,
        offset=skip,
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
        put_hotel_ok = await db.hotels.put_hotel(id_hotel, hotel_data)
        if not put_hotel_ok:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Hotel not found")
        await db.flush()
        await db.refresh()
        await db.commit()
        return {"status": "OK", "data": put_hotel_ok}

@router.patch("/{id_hotel}")
async def patch_hotels(
    db: DBDep,
    id_hotel: int = Path(description="The ID of the hotel."),
    hotel_data: HotelPatch = Body(embed=True, description="The hotel data."),
):
    data = hotel_data.model_dump(exclude_unset=True)

    if not data:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="No fields to update.")

    # Загружаем объект
    obj = await db.hotels.get(id_hotel)
    if not obj:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Hotel not found")

    try:
        # Частичное обновление
        await db.hotels.patch_hotel(obj, data)

        await db.flush()
        await db.refresh()
        await db.commit()
    except IntegrityError:
        await db.rollback()
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Update violates a constraint.",
        )

    return {"status": "OK", "data": obj}
@router.delete("/{hotel_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_hotel(
    db: DBDep,
    hotel_id: int,
):
    ok = await db.hotels.delete_hotels(hotel_id)
    if not ok:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="The hotel does not exist.")
    await db.commit()
    return None


